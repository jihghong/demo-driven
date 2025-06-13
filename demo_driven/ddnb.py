import argparse
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
import fnmatch

if sys.platform.startswith("win"):
    import asyncio
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

def save_dir_config(text: str):
    Path(TARGET_DIR_FILE).write_text(text)
    return text

def load_dir_config() -> str:
    try:
        return Path(TARGET_DIR_FILE).read_text().strip()
    except FileNotFoundError:
        return "demo"

def ddnbo():
    parser = argparse.ArgumentParser(description="Check for mismatches between notebook outputs and actual execution results, with options to fix them.")
    parser.add_argument("names", nargs="*", help="Check the specified notebooks, or check all if none are specified")
    parser.add_argument("-f", "--fix", action="store_true", help="Fix outputs if they mismatch actual execution results, otherwise keep the notebook untouched")
    parser.add_argument("-F", "--force", action="store_true", help="Force execution and overwrite all outputs with actual results")
    parser.add_argument("-d", "--dir", nargs="?", const="", help="Set or show the target directory containing notebooks.")
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

    demo_dir = load_dir_config()

    if args.names:
        all_files = list(Path(demo_dir).glob("*.ipynb"))
        for pattern in args.names:
            matches = [f for f in all_files if fnmatch.fnmatch(f.name, pattern + ".ipynb")]
            if not matches:
                print(f"{pattern}: not found")
            for ipynb_file in sorted(matches):
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
        ipynb_files = sorted(Path(demo_dir).glob("*.ipynb"))
        for ipynb_file in ipynb_files:
            original_nb = nbformat.read(ipynb_file, as_version=4)
            executed_nb = run_notebook(ipynb_file)
            compare_and_patch_outputs(
                original_nb,
                executed_nb,
                patch=args.fix or args.force,
                force=args.force,
                ipynb_file=ipynb_file
            )

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m demo_driven.ddnb <notebook.ipynb>", file=sys.stderr)
        sys.exit(1)

    ipynb_path = Path(sys.argv[1])
    if not ipynb_path.exists():
        print(f"Error: file not found: {ipynb_path}", file=sys.stderr)
        sys.exit(1)

    nb = run_notebook(ipynb_path)

    outputs = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            for output in cell.get("outputs", []):
                if output.output_type == "stream":
                    outputs.append(output.text)
                elif output.output_type in ("execute_result", "display_data"):
                    text = output.get("data", {}).get("text/plain")
                    if text:
                        outputs.append(text)
                elif output.output_type == "error":
                    outputs.append("\n".join(output.get("traceback", [])))

    print("\n".join(outputs), end='')

if __name__ == "__main__":
    main()
