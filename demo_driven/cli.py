# demo_driven/cli.py

import argparse
import difflib
import subprocess
from pathlib import Path
import sys

DEMO_DIR = Path.cwd() / "demo"


def run_demo(name: str):
    py_file = DEMO_DIR / f"{name}.py"
    out_file = DEMO_DIR / f"{name}.txt"
    html_file = DEMO_DIR / f"{name}.html"
    old_file = DEMO_DIR / f"{name}.txt.old"

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

        from difflib import HtmlDiff
        html = HtmlDiff().make_file(
            baseline.splitlines(), output.splitlines(),
            fromdesc=f"previous output ({name}.txt.old)",
            todesc=f"current output ({name}.txt)")

        html_file.write_text(html, encoding="utf-8")
        print(f"{name}: output changed, see {html_file.name}")


def accept_demo(name: str):
    html_file = DEMO_DIR / f"{name}.html"
    old_file = DEMO_DIR / f"{name}.txt.old"

    if not old_file.exists():
        print(f"{name}: nothing to accept")
        return

    for f in [html_file, old_file]:
        if f.exists():
            f.unlink()
    print(f"{name}: accepted")


def run_all():
    for file in sorted(DEMO_DIR.glob("*.py")):
        name = file.stem
        run_demo(name)


def accept_all():
    for file in sorted(DEMO_DIR.glob("*.py")):
        name = file.stem
        accept_demo(name)


def main():
    parser = argparse.ArgumentParser(description="Run and manage demo-driven output scripts")
    parser.add_argument("names", nargs="*", help="Run one or more demo scripts by name")
    parser.add_argument("-a", "--accept", action="store_true", help="Accept mode for positional names (or all if none specified)")
    parser.add_argument("-r", "--run-all", action="store_true", help="Run all demos")
    args = parser.parse_args()

    if args.accept:
        if args.names:
            for name in args.names:
                accept_demo(name)
        else:
            accept_all()
    elif args.run_all:
        if args.names:
            print("[WARN] Ignoring positional names when using -r/--run-all.")
        run_all()
    elif args.names:
        for name in args.names:
            run_demo(name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
