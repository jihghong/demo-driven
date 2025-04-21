# Demo Walkthrough

This folder demonstrates the Demo-Driven Development (DDD) workflow using real demo scripts and output files.

### Root folder
- Contains the original demo scripts: `hello.py` and `sorting.py`
- This represents the state **before any output has been generated**

If you run `ddrun` at this point, you will see output like:

```
hello: output saved
sorting: output saved
```

The outputs of the demo scripts are captured and saved as the initial baseline.
As a result, the directory now becomes like the contents of `created/`.

### `created/`

If you run `ddrun` again in this state, you will see:

```
hello: output matches saved result
sorting: output matches saved result
```
- Represents the initial output being locked in as the behavioral baseline

### `modified/`
Suppose the author modifies the demo scripts into the versions found in `modified/hello.py` and `modified/sorting.py`.

If you run `ddrun` in this state, you will see:

```
hello: output changed, see hello.html
sorting: output changed, see sorting.html
```

The output of each script is updated in `hello.txt` and `sorting.txt`, while the previous baseline is preserved as `hello.txt.old` and `sorting.txt.old`.
You can open the corresponding `.html` files to visually inspect the differences.

If the author later fixes the script to return to its original behavior and runs `ddrun` again, the output will be:

```
hello: output matches saved result
sorting: output matches saved result
```

The system detects that the output is now consistent with the baseline, so `.old` and `.html` files are automatically deleted.

### `accepted/`
If the author decides that the new output is correct and intentional, he or she can run `ddrun -a` in the modified state. This will produce:

```
hello: accepted
sorting: accepted
```

- The changes are confirmed and accepted using `ddrun -a`
- `.txt` files are updated with the new output
- `.old` and `.html` files are automatically deleted
- Represents a stable state where updated behavior is locked in

---

To explore the DDD workflow, you can walk through these folders and see how demo scripts evolve, how differences are detected, and how outputs are accepted or reverted.
