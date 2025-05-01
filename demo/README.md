# Demo Walkthrough

This folder demonstrates the Demo-Driven Development (DDD) workflow using real demo scripts and output files.

### Root folder
- Contains the original demo scripts: `hello.py`, `hello.ipynb`, `sorting.py`, and `sorting.ipynb`
- This represents the state **before any output has been generated**

Before running anything else, use `ddrun -d demo` to set the target directory. This will write a `.dddir` file to remember the setting for both `ddrun` and `ddnbo`.

If you run `ddrun` at this point, you will see output like:

```
hello.ipynb: output saved
hello.py: output saved
sorting.ipynb: output saved
sorting.py: output saved
```

The outputs of the demo scripts are captured and saved as the initial baseline.
As a result, the directory now becomes like the contents of `created/`.

### `created/`

If you run `ddrun` again in this state, you will see:

```
hello.ipynb: output matches saved result
hello.py: output matches saved result
sorting.ipynb: output matches saved result
sorting.py: output matches saved result
```

- Represents the initial output being locked in as the behavioral baseline

### `modified/`
Suppose the author modifies the demo scripts into the versions found in `modified/hello.py`, `modified/hello.ipynb`, `modified/sorting.py`, and `modified/sorting.ipynb`.

If you run `ddrun` in this state, you will see:

```
hello.ipynb: output changed, see hello.ipynb.html
hello.py: output changed, see hello.py.html
sorting.ipynb: output changed, see sorting.ipynb.html
sorting.py: output changed, see sorting.py.html
```

The output of each script is updated in `*.txt`, while the previous baseline is preserved as `.old` files.
You can open the corresponding `.html` files to visually inspect the differences.

### `reverted/`
Suppose the author has modified the scripts, but later changes them again so that, although the code might be different from the original, the output matches the original baseline.

If you run `ddrun` in this state, you will see:

```
hello.ipynb: output matches saved result
hello.py: output matches saved result
sorting.ipynb: output matches saved result
sorting.py: output matches saved result
```

- Regardless of code changes, identical output is treated as a reversion to the original behavior.
- `.old` and `.html` files are automatically deleted upon detecting the match.

### `accepted/`
If the author decides that the new outputs (from the modified scripts) are correct and intentional, he or she can run `ddrun -a` in the modified state. This will produce:

```
hello.ipynb: accepted
hello.py: accepted
sorting.ipynb: accepted
sorting.py: accepted
```

- The changes are confirmed and accepted using `ddrun -a`
- `.txt` files are updated with the new output
- `.old` and `.html` files are automatically deleted
- Represents a stable state where updated behavior is locked in

If you run `ddrun -a` again after accepting, you will see:

```
hello.ipynb: nothing to accept
hello.py: nothing to accept
sorting.ipynb: nothing to accept
sorting.py: nothing to accept
```

### `fixed/`
This folder illustrates how notebook outputs can be repaired using the `ddnbo` tool. `ddnbo` stands for **Demo-Driven Notebook Output** fixer.

For example, `hello.ipynb` has correct code but incorrect outputs stored in its cells. `sorting.ipynb` hasn't been executed yet, so its cells are missing output altogether. You can use `ddnbo` to detect and fix both situations.

Since `ddnbo` also reads the `.dddir` setting, it will continue using the same target directory `demo/` previously set by `ddrun -d demo`. You can also use `ddnbo -d demo` to set it.

First, run `ddnbo` without any options. This will only check notebook outputs against actual execution results without making any changes. You can see output like:

```
hello.ipynb: [1] mismatched
sorting.ipynb: [2][3][4][5] mismatched
```

Then run `ddnbo -f` to fix only the mismatched outputs:

```
hello.ipynb: outputs updated
sorting.ipynb: outputs updated
```

After fixing, you can re-run `ddnbo` to confirm that everything matches:

```
hello.ipynb: outputs matched
sorting.ipynb: outputs matched
```

If you want to force re-execution and overwrite all outputs regardless of match, use:

```
ddnbo -F
```

---

To explore the DDD workflow, you can walk through these folders and see how demo scripts evolve, how differences are detected, how outputs are reverted or accepted, and how notebook outputs can be automatically repaired using `ddnbo`.
