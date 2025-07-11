import argparse
from pathlib import Path
from demo_driven.ddrun import (
    load_target_dir_config, set_or_show_target_dir,
    glob_sorted, match_pattern,
    read_notebook, save_notebook, execute_notebook, notebook_cell_output_text
)

def compare_and_fix_outputs(ipynb_file: Path, fix: bool, force: bool):
    original_nb = read_notebook(ipynb_file)
    executed_nb = read_notebook(ipynb_file)  # copy
    execute_notebook(executed_nb)
    modified = False
    mismatched_cells = []
    code_index = 0
    for orig_cell, exec_cell in zip(original_nb.cells, executed_nb.cells):
        if orig_cell.cell_type != "code":
            continue
        code_index += 1

        if force:
            orig_cell["outputs"] = exec_cell.get("outputs", [])
            modified = True
        elif notebook_cell_output_text(orig_cell) != notebook_cell_output_text(exec_cell):
            mismatched_cells.append(code_index)
            if fix:
                orig_cell["outputs"] = exec_cell.get("outputs", [])
                modified = True

    if not fix and not force:
        if mismatched_cells:
            cells = "".join(f"[{i}]" for i in mismatched_cells)
            print(f"{ipynb_file.name}: {cells} mismatched")
        else:
            print(f"{ipynb_file.name}: outputs matched")
    else:
        if modified:
            save_notebook(original_nb, ipynb_file)
            print(f"{ipynb_file.name}: outputs updated")
        else:
            print(f"{ipynb_file.name}: no need to update")

def main():
    parser = argparse.ArgumentParser(description="Check for mismatches between notebook outputs and actual execution results, with options to fix them.")
    parser.add_argument("names", nargs="*", help="Check the specified notebooks, or check all if none are specified")
    parser.add_argument("-d", "--dir", nargs="?", const="", help="Set or show the target directory containing notebooks.")
    parser.add_argument("-f", "--fix", action="store_true", help="Fix outputs if they mismatch actual execution results, otherwise keep the notebook untouched")
    parser.add_argument("-F", "--force", action="store_true", help="Force execution and overwrite all outputs with actual results")
    args = parser.parse_args()

    original_dddir, demo_dir = load_target_dir_config()

    if args.dir is not None:
        return set_or_show_target_dir(demo_dir, args.dir, bool(args.names))

    all_ipynb_files = glob_sorted(demo_dir, order={".ipynb": ".ipynb"})
    if args.names:
        for pattern in args.names:
            if matched := match_pattern(pattern, all_ipynb_files):
                for ipynb_file in matched:
                    compare_and_fix_outputs(ipynb_file, args.fix, args.force)
    else:
        for ipynb_file in all_ipynb_files:
            compare_and_fix_outputs(ipynb_file, args.fix, args.force)

if __name__ == "__main__":
    main()
