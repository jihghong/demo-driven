import argparse
import difflib
import subprocess
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

CONFIG_FILE = ".ddrun_dir"


def save_dir_config(demo_dir: Path):
    relative = demo_dir.relative_to(Path.cwd())
    Path(CONFIG_FILE).write_text(str(relative))
    print(f"Target directory is set to '{relative}'")


def load_dir_config() -> Path:
    try:
        name = Path(CONFIG_FILE).read_text().strip()
        return Path.cwd() / name
    except FileNotFoundError:
        return Path.cwd() / "demo"


def run_demo(name: str, demo_dir: Path):
    py_file = demo_dir / f"{name}.py"
    out_file = demo_dir / f"{name}.py.txt"
    html_file = demo_dir / f"{name}.py.html"
    old_file = demo_dir / f"{name}.py.txt.old"

    if not py_file.exists():
        print(f"{name}.py: script not found")
        return

    result = subprocess.run(
        [sys.executable, str(py_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output = result.stdout

    if not out_file.exists():
        out_file.write_text(output)
        print(f"{name}.py: output saved")
        return

    if old_file.exists():
        baseline = old_file.read_text()
    else:
        baseline = out_file.read_text()

    if output == baseline:
        print(f"{name}.py: output matches saved result")
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
            fromdesc=f"previous output ({name}.py.txt.old)",
            todesc=f"current output ({name}.py.txt)"
        )

        html_file.write_text(html, encoding="utf-8")
        print(f"{name}.py: output changed, see {html_file.name}")


def run_ipynb_demo(name: str, demo_dir: Path):
    ipynb_file = demo_dir / f"{name}.ipynb"
    if not ipynb_file.exists():
        print(f"{name}.ipynb: notebook not found")
        return

    out_file = demo_dir / f"{name}.ipynb.txt"
    html_file = demo_dir / f"{name}.ipynb.html"
    old_file = demo_dir / f"{name}.ipynb.txt.old"

    nb = nbformat.read(ipynb_file, as_version=4)
    client = NotebookClient(nb)
    client.execute()

    outputs = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            for output in cell.get("outputs", []):
                if output.output_type == "stream":
                    outputs.append(output.text)
                elif output.output_type in ("execute_result", "display_data"):
                    data = output.get("data", {})
                    text = data.get("text/plain")
                    if text:
                        outputs.append(text)
                elif output.output_type == "error":
                    outputs.append("\n".join(output.get("traceback", [])))

    output = "\n".join(outputs)

    if not out_file.exists():
        out_file.write_text(output)
        print(f"{name}.ipynb: output saved")
        return

    if old_file.exists():
        baseline = old_file.read_text()
    else:
        baseline = out_file.read_text()

    if output == baseline:
        print(f"{name}.ipynb: output matches saved result")
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
            fromdesc=f"previous output ({name}.ipynb.txt.old)",
            todesc=f"current output ({name}.ipynb.txt)"
        )

        html_file.write_text(html, encoding="utf-8")
        print(f"{name}.ipynb: output changed, see {html_file.name}")


def accept_demo(name: str, demo_dir: Path, suffix: str):
    removed = False
    if suffix == ".py":
        exts = ["py.txt.old", "py.html"]
    elif suffix == ".ipynb":
        exts = ["ipynb.txt.old", "ipynb.html"]
    else:
        exts = []

    for ext in exts:
        file = demo_dir / f"{name}.{ext}"
        if file.exists():
            file.unlink()
            removed = True

    if removed:
        print(f"{name}{suffix}: accepted")
    else:
        print(f"{name}{suffix}: nothing to accept")


def run_all(demo_dir: Path):
    files = sorted(list(demo_dir.glob("*.py")) + list(demo_dir.glob("*.ipynb")))
    for file in files:
        name = file.stem
        if file.suffix == ".py":
            run_demo(name, demo_dir)
        elif file.suffix == ".ipynb":
            run_ipynb_demo(name, demo_dir)


def accept_all(demo_dir: Path):
    files = sorted(list(demo_dir.glob("*.py")) + list(demo_dir.glob("*.ipynb")))
    for file in files:
        name = file.stem
        if file.suffix == ".py":
            accept_demo(name, demo_dir, suffix=".py")
        elif file.suffix == ".ipynb":
            accept_demo(name, demo_dir, suffix=".ipynb")


def main():
    parser = argparse.ArgumentParser(description="Run demo scripts and manage their outputs")
    parser.add_argument("names", nargs="*", help="Run the specified demo scripts, or run all if none are specified")
    parser.add_argument("-a", "--accept", action="store_true", help="Accept the outputs of specified demo scripts, or accept all if none are specified")
    parser.add_argument("-d", "--dir", help="Set the target directory containing demo scripts")
    args = parser.parse_args()

    if args.dir:
        demo_dir = Path.cwd() / args.dir
        save_dir_config(demo_dir)
        return

    demo_dir = load_dir_config()

    if args.accept:
        if args.names:
            for name in args.names:
                if (demo_dir / f"{name}.py").exists():
                    accept_demo(name, demo_dir, suffix=".py")
                if (demo_dir / f"{name}.ipynb").exists():
                    accept_demo(name, demo_dir, suffix=".ipynb")
                if not (demo_dir / f"{name}.py").exists() and not (demo_dir / f"{name}.ipynb").exists():
                    print(f"{name}: script not found")
        else:
            accept_all(demo_dir)
    elif args.names:
        for name in args.names:
            if (demo_dir / f"{name}.py").exists():
                run_demo(name, demo_dir)
            if (demo_dir / f"{name}.ipynb").exists():
                run_ipynb_demo(name, demo_dir)
            if not (demo_dir / f"{name}.py").exists() and not (demo_dir / f"{name}.ipynb").exists():
                print(f"{name}: script not found")
    else:
        run_all(demo_dir)


if __name__ == "__main__":
    main()
