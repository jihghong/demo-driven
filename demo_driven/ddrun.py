import os
import sys
from pathlib import Path
import argparse
import configparser
import subprocess
import re
import shlex
import fnmatch
import difflib
import nbformat
from nbclient import NotebookClient

import logging
logger = logging.getLogger(__name__)

if sys.platform.startswith("win"):  # nbclient issue #128, pyzmq issue #1554
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TARGET_DIR_FILE = Path(".dddir")
DEFAULT_TEXT_ENCODING = "utf-8"
PYTHON_UTF8_ENV = os.environ.copy()
PYTHON_UTF8_ENV.setdefault("PYTHONUTF8", "1")
PYTHON_UTF8_ENV.setdefault("PYTHONIOENCODING", DEFAULT_TEXT_ENCODING)

def load_target_dir_config():  # -> original_dddir, demo_dir
    try:
        return (demo_dir := TARGET_DIR_FILE.read_text(encoding=DEFAULT_TEXT_ENCODING).strip()), demo_dir
    except:
        return None, "showcase"

def save_dir_config(args_dir: str):
    TARGET_DIR_FILE.write_text(args_dir, encoding=DEFAULT_TEXT_ENCODING)

def restore_target_dir_config(original_dddir):
    if original_dddir is None:
        TARGET_DIR_FILE.unlink(missing_ok=True)
    else:
        TARGET_DIR_FILE.write_text(original_dddir, encoding=DEFAULT_TEXT_ENCODING)

def set_or_show_target_dir(demo_dir: str, args_dir: str, extra_ignored: bool):
    if args_dir:
        save_dir_config(args_dir)
        if extra_ignored:
            print(f'Target directory is set to "{args_dir}", extra arguments ignored')
        else:
            print(f'Target directory is set to "{args_dir}"')
    else:
        print(f'Current target directory: "{demo_dir}"')

def read_demo_driven_ini():
    config = configparser.ConfigParser()
    ini = Path("demo_driven.ini")
    if ini.exists():
        config.read(ini, encoding=DEFAULT_TEXT_ENCODING)
    return config

demo_driven_config = read_demo_driven_ini()

def ini_bash_path():
    if "bash" in demo_driven_config:
        bash_section = demo_driven_config["bash"]
        if "command" in bash_section:
            return shlex.split(bash_section["command"])
    return ["bash"]

BASH = ini_bash_path()

SUPPRESSED_PATTERNS = [
    re.compile(r"^.*Assertion failed: .+ \[\d+\] \(.+?:\d+\).*\n?", re.MULTILINE)
]

def read_notebook(ipynb_file: Path):
    return nbformat.read(ipynb_file, as_version=4)

def save_notebook(nb, ipynb_file: Path):
    nbformat.write(nb, ipynb_file)

def execute_notebook(nb):
    client = NotebookClient(nb)
    client.execute()

def notebook_outputs(nb):
    return [notebook_cell_output_text(cell) for cell in nb.cells if cell.cell_type == "code"]

def notebook_cell_output_text(cell):
    text = ''
    prev_type = None
    for output in cell.get("outputs", []):
        if prev_type is not None and prev_type != output.output_type:
            text += "\n"
        if output.output_type == "stream":
            text += output.text
        elif output.output_type in ("execute_result", "display_data"):
            text += output.get("data", {}).get("text/plain", '')
        elif output.output_type == "error":
            text += "\n".join(output.get("traceback", []))
        prev_type = output.output_type
    return text

def run_script(script_file: Path):
    match script_file.suffix:
        case ".py":
            output = subprocess.run(
                [sys.executable, script_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=DEFAULT_TEXT_ENCODING,
                env=PYTHON_UTF8_ENV
            ).stdout
        case ".ipynb":
            nb = read_notebook(script_file)
            execute_notebook(nb)
            output = "\n".join(notebook_outputs(nb))
        case ".sh":
            output = subprocess.run(
                BASH + [script_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=DEFAULT_TEXT_ENCODING
            ).stdout
    logger.debug(f"before {output!r}")
    for pattern in SUPPRESSED_PATTERNS:
        output = pattern.sub("", output)
    logger.debug(f"after  {output!r}")
    save_output_and_diff(script_file, output)

def save_output_and_diff(script_file: Path, output: str):
    out_file = script_file.with_name(script_file.name + ".txt")
    old_file = script_file.with_name(script_file.name + ".tx~")
    html_file = script_file.with_name(script_file.name + ".html")
    if not out_file.exists():
        out_file.write_text(output, encoding=DEFAULT_TEXT_ENCODING)
        print(f"{script_file.name}: output saved")
    else:
        if old_file.exists():
            baseline = old_file.read_text(encoding=DEFAULT_TEXT_ENCODING)
        else:
            baseline = out_file.read_text(encoding=DEFAULT_TEXT_ENCODING)
        if output == baseline:
            logger.debug(f"{script_file.name}: output matches saved result")
            print(f"{script_file.name}: output matches saved result")
            if old_file.exists():
                old_file.replace(out_file)
            for f in [html_file, old_file]:
                f.unlink(missing_ok=True)
        else:
            if not old_file.exists():
                out_file.rename(old_file)
            out_file.write_text(output, encoding=DEFAULT_TEXT_ENCODING)
            html = difflib.HtmlDiff().make_file(
                baseline.splitlines(), output.splitlines(),
                fromdesc=f"previous output ({old_file.name})",
                todesc=f"current output ({out_file.name})"
            )
            html_file.write_text(html, encoding=DEFAULT_TEXT_ENCODING)
            logger.debug(f"{script_file.name}: output changed, see {html_file.name}")
            print(f"{script_file.name}: output changed, see {html_file.name}")

def accept_script(script_file: Path):
    found = False
    for suffix in [".tx~", ".html"]:
        file = script_file.with_name(script_file.name + suffix)
        if file.exists():
            file.unlink()
            found = True
    if found:
        print(f"{script_file.name}: accepted")
    else:
        print(f"{script_file.name}: nothing to accept")

def glob_sorted(demo_dir: str, order={ ".py":".0", ".ipynb":".1", ".sh":".2" }):
    return sorted([f for f in Path(demo_dir).glob("*") if f.suffix in order], key=lambda f: f.stem + order[f.suffix])

def match_pattern(pattern: str, all_files: list[Path]):
    return [f for f in all_files if fnmatch.fnmatch(f.name, pattern) or fnmatch.fnmatch(f.stem, pattern)]

def main():
    parser = argparse.ArgumentParser(
        description="Run demo scripts and manage their outputs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("names", nargs="*", help="Run the specified demo scripts, or run all if none are specified")
    parser.add_argument("-d", "--dir", nargs="?", const="", help="Set or show the target directory containing demo scripts")
    parser.add_argument("-a", "--accept", action="store_true", help="Accept the outputs of specified demo scripts, or accept all if none are specified")
    args = parser.parse_args()

    original_dddir, demo_dir = load_target_dir_config()

    if args.dir is not None:
        return set_or_show_target_dir(demo_dir, args.dir, bool(args.names))

    all_script_files = glob_sorted(demo_dir)
    if args.names:
        for pattern in args.names:
            if matched := match_pattern(pattern, all_script_files):
                if args.accept:
                    for script_file in matched:
                        accept_script(script_file)
                else:
                    for script_file in matched:
                        run_script(script_file)
                        restore_target_dir_config(original_dddir)
            else:
                print(f"{pattern}: not found")
    else:
        if args.accept:
            for script_file in all_script_files:
                accept_script(script_file)
        else:
            for script_file in all_script_files:
                run_script(script_file)
                restore_target_dir_config(original_dddir)

if __name__ == "__main__":
    main()
