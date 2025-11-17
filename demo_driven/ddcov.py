import os
import sys
import argparse
from pathlib import Path
import coverage
import subprocess
import bashlex
import re
import runpy

from demo_driven.ddrun import (
    demo_driven_config, BASH, DEFAULT_TEXT_ENCODING, PYTHON_UTF8_ENV,
    load_target_dir_config, set_or_show_target_dir, restore_target_dir_config,
    glob_sorted, match_pattern,
    read_notebook, execute_notebook, notebook_outputs,
    save_output_and_diff
)

import logging
logger = logging.getLogger(__name__)

SUPPRESSED_PATTERNS = [
    re.compile(r"^.*Assertion failed: .+ \[\d+\] \(.+?:\d+\).*\n?", re.MULTILINE),
    re.compile(
        r"^.*coverage.control.py:\d+: CoverageWarning: No data was collected.*\n\s+self._warn\(.*\).*$\n?",
        re.MULTILINE,
    ),
]

COVERAGE_SECTION = "coverage-cli"

def ini_coverage_section():
    if COVERAGE_SECTION in demo_driven_config:
        return demo_driven_config[COVERAGE_SECTION]
    return {}

registered_cli = ini_coverage_section()

def transform_shell_for_coverage(script_text: str) -> str:
    try:
        parts = bashlex.parse(script_text)
    except Exception:
        return script_text
    if not registered_cli:
        return script_text

    all_nodes = []
    for part in parts:
        queue = [part]
        while queue:
            node = queue.pop()
            if isinstance(node, bashlex.ast.node):
                if node.kind == "command":
                    all_nodes.append(node)
                if hasattr(node, "parts"):
                    queue.extend(node.parts)

    all_nodes.sort(key=lambda n: n.pos[0], reverse=True)

    text = script_text
    for node in all_nodes:
        words = [w.word for w in node.parts if hasattr(w, 'word')]
        if words and words[0] in registered_cli:
            words.insert(0, "tocov")
            span_start, span_end = node.pos
            text = text[:span_start] + " ".join(words) + text[span_end:]

    return text

def instrument_python_cell(nb):
    cov_prefix = [
        "import coverage",
        "cov = coverage.Coverage(omit=['*/ipykernel*/*.py'])",
        "cov.set_option('run:parallel', True)",
        "cov._warn_no_data = False",
        "cov._warn_preimported_source = False",
        "cov._warn_unimported_source = False",
        "cov.start()",
    ]
    cov_suffix = [
        "cov.stop()",
        "cov.save()"
    ]

    last_python_code_cell = None
    for cell in nb.cells:
        if cell.cell_type == "code":
            lines = cell.source.splitlines()
            if lines and lines[0].strip().startswith("%%bash"):
                bash_script = "\n".join(lines[1:])
                transformed = transform_shell_for_coverage(bash_script)
                cell_lines = [lines[0]] + transformed.splitlines()
                cell.source = "\n".join(cell_lines)
            else:
                new_lines = []
                if last_python_code_cell is None:
                    new_lines = cov_prefix

                for line in lines:
                    if line.strip().startswith("!"):
                        transformed = transform_shell_for_coverage(line.strip()[1:])
                        new_lines.append("!" + transformed)
                    else:
                        new_lines.append(line)
                cell.source = "\n".join(new_lines)
            last_python_code_cell = cell
        if last_python_code_cell is not None:
            last_python_code_cell.source = "\n".join([last_python_code_cell.source] + cov_suffix)

def run_script_with_coverage(script_file: Path):
    match script_file.suffix:
        case ".py":
            output = subprocess.run(
                [sys.executable, "-m", "coverage", "run", "--parallel-mode", "--omit", script_file, script_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=DEFAULT_TEXT_ENCODING,
                env=PYTHON_UTF8_ENV
            ).stdout
        case ".ipynb":
            nb = read_notebook(script_file)
            instrument_python_cell(nb)
            execute_notebook(nb)
            output = "\n".join(notebook_outputs(nb))
        case ".sh":
            original = script_file.read_text(encoding=DEFAULT_TEXT_ENCODING)
            transformed = transform_shell_for_coverage(original)
            output = subprocess.run(
                BASH,
                input=transformed,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=DEFAULT_TEXT_ENCODING,
                env=PYTHON_UTF8_ENV
            ).stdout
    logger.debug(f"before {output!r}")
    for pattern in SUPPRESSED_PATTERNS:
        output = pattern.sub("", output)
    logger.debug(f"after  {output!r}")
    save_output_and_diff(script_file, output)

def main():
    parser = argparse.ArgumentParser(
        description="Run demo scripts with coverage",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("names", nargs="*", help="Run the specified demo scripts, or run all if none are specified")
    parser.add_argument("-d", "--dir", nargs="?", const="", help="Set or show the target demo directory containing demo scripts")
    args = parser.parse_args()

    original_dddir, demo_dir = load_target_dir_config()

    if args.dir is not None:
        return set_or_show_target_dir(demo_dir, args.dir, bool(args.names))

    all_script_files = glob_sorted(demo_dir)
    if args.names:
        for pattern in args.names:
            if matched := match_pattern(pattern, all_script_files):
                for script_file in matched:
                    run_script_with_coverage(script_file)
                    restore_target_dir_config(original_dddir)
            else:
                print(f"{pattern}: not found")
    else:
        for script_file in all_script_files:
            run_script_with_coverage(script_file)
            restore_target_dir_config(original_dddir)
    cov = coverage.Coverage()
    cov.combine()

def tocov():
    args = sys.argv[1:]

    if not args:
        print("tocov: no command provided")
        sys.exit(1)

    cli_name = args[0]

    if cli_name not in registered_cli:
        print(f"tocov: command '{cli_name}' not registered in [{COVERAGE_SECTION}] of demo_driven.ini")
        sys.exit(1)

    entry = registered_cli[cli_name]
    mod, _, func = entry.partition(":")

    cov = coverage.Coverage()
    cov.set_option("run:parallel", True)
    cov._warn_no_data = False
    cov._warn_preimported_source = False
    cov._warn_unimported_source = False
    cov.start()
    sys.argv = [cli_name] + args[1:]
    if not func:
        runpy.run_module(mod, run_name="__main__")
    else:
        module = __import__(mod, fromlist=[func])
        getattr(module, func)()
    cov.stop()
    cov.save()

if __name__ == "__main__":
    main()
