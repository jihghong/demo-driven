import argparse
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TARGET_DIR_FILE = ".dddir"

def run_notebook(ipynb_file: Path):
    nb = nbformat.read(ipynb_file, as_version=4)
    client = NotebookClient(nb)
    client.execute()
    return nb

def compare_and_patch_outputs(original_nb, executed_nb, patch: bool, force: bool, ipynb_file: Path):
    mismatched_cells = []
    code_index = 0
    for orig_cell, exec_cell in zip(original_nb.cells, executed_nb.cells):
        if orig_cell.cell_type != "code":
            continue
        code_index += 1
        orig_outputs = orig_cell.get("outputs", [])
        exec_outputs = exec_cell.get("outputs", [])

        if force or orig_outputs != exec_outputs:
            mismatched_cells.append(code_index)
            if patch:
                orig_cell["outputs"] = exec_outputs

    if not patch:
        if mismatched_cells:
            cells = "".join(f"[{i}]" for i in mismatched_cells)
            print(f"{ipynb_file.name}: {cells} mismatched")
        else:
            print(f"{ipynb_file.name}: outputs matched")
    else:
        if mismatched_cells:
            nbformat.write(original_nb, ipynb_file)
            print(f"{ipynb_file.name}: outputs updated")
        else:
            print(f"{ipynb_file.name}: outputs matched, no update needed")

def save_dir_config(path: Path):
    relative = path.relative_to(Path.cwd())
    Path(TARGET_DIR_FILE).write_text(str(relative))
    print(f"Target directory set to '{relative}'")

def load_dir_config() -> Path:
    return Path((Path.cwd() / TARGET_DIR_FILE).read_text().strip())

def main():
    parser = argparse.ArgumentParser(description="Check for mismatches between notebook outputs and actual execution results, with options to fix them.")
    parser.add_argument("names", nargs="*", help="Check the specified notebooks, or check all if none are specified")
    parser.add_argument("-f", "--fix", action="store_true", help="Fix outputs if they mismatch actual execution results, otherwise keep the notebook untouched")
    parser.add_argument("-F", "--force", action="store_true", help="Force execution and overwrite all outputs with actual results")
    parser.add_argument("-d", "--dir", help="Set the target directory containing notebooks.")
    args = parser.parse_args()

    if args.dir:
        demo_dir = Path.cwd() / args.dir
        save_dir_config(demo_dir)
        return

    demo_dir = load_dir_config() if (Path.cwd() / TARGET_DIR_FILE).exists() else Path.cwd()

    if args.names:
        ipynb_files = [demo_dir / f"{name}.ipynb" for name in args.names]
    else:
        ipynb_files = sorted(demo_dir.glob("*.ipynb"))

    for ipynb_file in ipynb_files:
        if ipynb_file.exists():
            original_nb = nbformat.read(ipynb_file, as_version=4)
            executed_nb = run_notebook(ipynb_file)
            compare_and_patch_outputs(
                original_nb,
                executed_nb,
                patch=args.fix or args.force,
                force=args.force,
                ipynb_file=ipynb_file
            )
        else:
            print(f"{ipynb_file.name}: notebook not found")

if __name__ == "__main__":
    main()
