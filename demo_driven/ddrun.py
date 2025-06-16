import argparse
import difflib
import subprocess
import sys
import shlex
import re
import os
from pathlib import Path
import fnmatch

if sys.platform.startswith("win"):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TARGET_DIR_FILE = ".dddir"
EXTENSION_MAP_FILE = "ddrun.ini"
RESERVED_SUFFIXES = {".txt", ".html", ".old", ".ini"}
PATH_TOKEN = "DDRUN___PATH___DDRUN"
PYTHON_TOKEN = "DDRUN___PYTHON___DDRUN"

SUPPRESSED_PATTERNS = [
    re.compile(r"^.*Assertion failed: .+ \[\d+\] \(.+?:\d+\).*\n?", re.MULTILINE),
    re.compile(
        r"^.*coverage.control.py:\d+: CoverageWarning: No data was collected.*\n\s+self._warn\(.*\).*$\n?",
        re.MULTILINE,
    ),
]

def wrap_coverage_if_needed(tokens):
    if os.environ.get("DEMO_DRIVEN_WITH_COVERAGE") != "1":
        return tokens
    try:
        idx = tokens.index(PYTHON_TOKEN)
        if idx + 1 < len(tokens) and tokens[idx + 1] == "-c":
            return tokens  # skip coverage for -c commands
        return ["coverage", "run"] + tokens[idx + 1:]
    except ValueError:
        return tokens

def load_extension_map():
    extmap = {}
    path = Path(EXTENSION_MAP_FILE)
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                print(f"Invalid line in {EXTENSION_MAP_FILE}: {line}")
                continue
            ext, cmd = line.split("=", 1)
            ext = ext.strip()
            cmd = cmd.strip()
            if not ext.startswith("."):
                ext = "." + ext
            if ext in RESERVED_SUFFIXES:
                print(f"Error: extension {ext} is reserved and cannot be redefined")
                sys.exit(1)
            tokens = shlex.split(cmd, comments=True)
            tokens = [
                PYTHON_TOKEN if t == "{python}" else PATH_TOKEN if t == "{path}" else t
                for t in tokens
            ]
            extmap[ext] = tokens

    if ".py" not in extmap:
        extmap[".py"] = [PYTHON_TOKEN, PATH_TOKEN]

    if ".ipynb" not in extmap:
        extmap[".ipynb"] = [PYTHON_TOKEN, "-m", "demo_driven.ddnb", PATH_TOKEN]

    return extmap

def generate_supported_extensions_help():
    extmap = load_extension_map()
    text = "\nSupported extensions (configurable via ddrun.ini):\n\n"
    for ext, tokens in extmap.items():
        if ext in RESERVED_SUFFIXES:
            continue
        cmdline = shlex.join(tokens)
        cmdline = cmdline.replace(PYTHON_TOKEN, "{python}").replace(PATH_TOKEN, "{path}")
        text += f"{ext.lstrip('.')} = {cmdline}\n"
    return text

def save_dir_config(demo_dir_str: str):
    Path(TARGET_DIR_FILE).write_text(demo_dir_str)
    return demo_dir_str

def load_dir_config() -> str:
    try:
        return Path(TARGET_DIR_FILE).read_text().strip()
    except FileNotFoundError:
        return "demo"

def is_executable_script(file: Path, extmap):
    if file.suffix in RESERVED_SUFFIXES:
        return False
    return file.suffix in extmap

def run_script(name: str, demo_dir: str, extmap, original_dddir: str):
    for ext, tokens in extmap.items():
        file = Path(demo_dir) / f"{name}{ext}"
        if not file.exists():
            continue

        out_file = Path(demo_dir) / f"{name}{ext}.txt"
        html_file = Path(demo_dir) / f"{name}{ext}.html"
        old_file = Path(demo_dir) / f"{name}{ext}.txt.old"

        tokens = wrap_coverage_if_needed(tokens)
        cmd = [
            sys.executable if t == PYTHON_TOKEN else str(file) if t == PATH_TOKEN else t
            for t in tokens
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = result.stdout
        for pattern in SUPPRESSED_PATTERNS:
            output = pattern.sub("", output)

        if not out_file.exists():
            out_file.write_text(output)
            print(f"{name}{ext}: output saved")
        else:
            if old_file.exists():
                baseline = old_file.read_text()
            else:
                baseline = out_file.read_text()

            if output == baseline:
                print(f"{name}{ext}: output matches saved result")
                if old_file.exists():
                    old_file.replace(out_file)
                for f in [html_file, old_file]:
                    if f.exists():
                        f.unlink()
            else:
                if not old_file.exists():
                    out_file.rename(old_file)
                out_file.write_text(output)
                html = difflib.HtmlDiff().make_file(
                    baseline.splitlines(), output.splitlines(),
                    fromdesc=f"previous output ({name}{ext}.txt.old)",
                    todesc=f"current output ({name}{ext}.txt)"
                )
                html_file.write_text(html, encoding="utf-8")
                print(f"{name}{ext}: output changed, see {html_file.name}")

        if original_dddir is not None:
            Path(TARGET_DIR_FILE).write_text(original_dddir)
        else:
            Path(TARGET_DIR_FILE).unlink(missing_ok=True)

def accept_script(name: str, demo_dir: str, extmap):
    accepted = False
    for ext in extmap:
        script_file = Path(demo_dir) / f"{name}{ext}"
        if script_file.exists():
            found = False
            for suffix in [".txt.old", ".html"]:
                file = Path(demo_dir) / f"{name}{ext}{suffix}"
                if file.exists():
                    file.unlink()
                    found = True
            if found:
                print(f"{name}{ext}: accepted")
                accepted = True
            else:
                print(f"{name}{ext}: nothing to accept")

def accept_all(demo_dir: str, extmap):
    all_files = Path(demo_dir).glob("*")
    script_names = set(f.stem for f in all_files if is_executable_script(f, extmap))
    for name in sorted(script_names):
        accept_script(name, demo_dir, extmap)

def main(coverage=False):
    parser = argparse.ArgumentParser(
        description="Run demo scripts and manage outputs, and collect execution coverage" if coverage else "Run demo scripts and manage their outputs",
        epilog=generate_supported_extensions_help(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="ddcov" if coverage else "ddrun"
    )
    parser.add_argument("names", nargs="*", help="Run the specified demo scripts, or run all if none are specified")
    parser.add_argument("-a", "--accept", action="store_true", help="Accept the outputs of specified demo scripts, or accept all if none are specified")
    parser.add_argument("-d", "--dir", nargs="?", const="", help="Set or show the target directory containing demo scripts")
    args = parser.parse_args()

    if args.dir is not None:
        if args.dir.strip() == "":
            current = Path(TARGET_DIR_FILE).read_text().strip() if Path(TARGET_DIR_FILE).exists() else "demo"
            print(f'Current target directory: "{current}"')
        else:
            result = save_dir_config(args.dir)
            if args.names:
                print(f'Target directory is set to "{result}", extra arguments ignored')
            else:
                print(f'Target directory is set to "{result}"')
        return

    original_dddir = Path(TARGET_DIR_FILE).read_text() if Path(TARGET_DIR_FILE).exists() else None

    try:
        extmap = load_extension_map()
        demo_dir = load_dir_config()

        if args.accept:
            if args.names:
                for name in args.names:
                    accept_script(name, demo_dir, extmap)
            else:
                accept_all(demo_dir, extmap)
            return

        if args.names:
            all_files = list(Path(demo_dir).glob("*"))
            script_names = set()
            for pattern in args.names:
                matches = [f.stem for f in all_files if fnmatch.fnmatch(f.name, pattern + ".*") and is_executable_script(f, extmap)]
                if not matches:
                    print(f"{pattern}: not found")
                script_names.update(matches)
            for name in sorted(script_names):
                run_script(name, demo_dir, extmap, original_dddir)
        else:
            all_files = Path(demo_dir).glob("*")
            script_names = set(f.stem for f in all_files if is_executable_script(f, extmap))
            for name in sorted(script_names):
                run_script(name, demo_dir, extmap, original_dddir)

    finally:
        pass

def ddcov():
    os.environ["DEMO_DRIVEN_WITH_COVERAGE"] = "1"
    main(coverage=True)

if __name__ == "__main__":
    main()
