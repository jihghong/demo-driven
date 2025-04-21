# demo_driven/cli.py

import argparse
import difflib
import subprocess
from pathlib import Path
import sys

CONFIG_FILE = ".ddrun_dir"

def save_dir_config(demo_dir: Path):
    Path(CONFIG_FILE).write_text(demo_dir.name)

def load_dir_config() -> Path:
    try:
        name = Path(CONFIG_FILE).read_text().strip()
        return Path.cwd() / name
    except FileNotFoundError:
        return Path.cwd() / "demo"

def run_demo(name: str, demo_dir: Path):
    py_file = demo_dir / f"{name}.py"
    out_file = demo_dir / f"{name}.txt"
    html_file = demo_dir / f"{name}.html"
    old_file = demo_dir / f"{name}.txt.old"

    if not py_file.exists():
        print(f"{name}: script not found")
        return

    result = subprocess.run([sys.executable, str(py_file)], capture_output=True, text=True)
    output = result.stdout

    if not out_file.exists():
        out_file.write_text(output)
        print(f"{name}: output saved")
        return

    if old_file.exists():
        baseline = old_file.read_text()
    else:
        baseline = out_file.read_text()

    if output == baseline:
        print(f"{name}: output matches saved result")
        for f in [html_file, old_file]:
            if f.exists():
                f.unlink()
    else:
        if not old_file.exists():
            out_file.rename(old_file)
        out_file.write_text(output)

        html = difflib.HtmlDiff().make_file(
            baseline.splitlines(), output.splitlines(),
            fromdesc=f"previous output ({name}.txt.old)",
            todesc=f"current output ({name}.txt)")

        html_file.write_text(html, encoding="utf-8")
        print(f"{name}: output changed, see {html_file.name}")

def accept_demo(name: str, demo_dir: Path):
    html_file = demo_dir / f"{name}.html"
    old_file = demo_dir / f"{name}.txt.old"

    if not old_file.exists():
        print(f"{name}: nothing to accept")
        return

    for f in [html_file, old_file]:
        if f.exists():
            f.unlink()
    print(f"{name}: accepted")

def run_all(demo_dir: Path):
    for file in sorted(demo_dir.glob("*.py")):
        name = file.stem
        run_demo(name, demo_dir)

def accept_all(demo_dir: Path):
    for file in sorted(demo_dir.glob("*.py")):
        name = file.stem
        accept_demo(name, demo_dir)

def main():
    parser = argparse.ArgumentParser(description="Run and manage demo-driven output scripts")
    parser.add_argument("names", nargs="*", help="Run one or more demo scripts by name")
    parser.add_argument("-a", "--accept", action="store_true", help="Accept mode for positional names (or all if none specified)")
    parser.add_argument("-d", "--dir", help="Directory containing demo scripts")
    args = parser.parse_args()

    if args.dir:
        demo_dir = Path.cwd() / args.dir
        save_dir_config(demo_dir)
    else:
        demo_dir = load_dir_config()

    if args.accept:
        if args.names:
            for name in args.names:
                accept_demo(name, demo_dir)
        else:
            accept_all(demo_dir)
    elif args.names:
        for name in args.names:
            run_demo(name, demo_dir)
    else:
        run_all(demo_dir)


if __name__ == "__main__":
    main()