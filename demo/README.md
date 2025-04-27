# Demo Walkthrough

This folder demonstrates the Demo-Driven Development (DDD) workflow using real demo scripts and output files.

### Root folder
- Contains the original demo scripts: `hello.py`, `sorting.py`, and `sorting.ipynb`
- This represents the state **before any output has been generated**

If you run `ddrun` at this point, you will see output like:

```
hello.py: output saved
sorting.ipynb: output saved
sorting.py: output saved
```

The outputs of the demo scripts are captured and saved as the initial baseline.
As a result, the directory now becomes like the contents of `created/`.

### `created/`

If you run `ddrun` again in this state, you will see:

```
hello.py: output matches saved result
sorting.ipynb: output matches saved result
sorting.py: output matches saved result
```

- Represents the initial output being locked in as the behavioral baseline

### `modified/`
Suppose the author modifies the demo scripts into the versions found in `modified/hello.py`, `modified/sorting.py`, and `modified/sorting.ipynb`.

If you run `ddrun` in this state, you will see:

```
hello.py: output changed, see hello.py.html
sorting.ipynb: output changed, see sorting.ipynb.html
sorting.py: output changed, see sorting.py.html
```

The output of each script is updated in `hello.py.txt`, `sorting.ipynb.txt`, and `sorting.py.txt`, while the previous baseline is preserved as `.old` files.
You can open the corresponding `.html` files to visually inspect the differences.

### `reverted/`
Suppose the author has modified the scripts, but later changes them again so that, although the code might be different from the original, the output matches the original baseline.

If you run `ddrun` in this state, you will see:

```
hello.py: output matches saved result
sorting.ipynb: output matches saved result
sorting.py: output matches saved result
```

- Regardless of code changes, identical output is treated as a reversion to the original behavior.
- `.old` and `.html` files are automatically deleted upon detecting the match.

### `accepted/`
If the author decides that the new outputs (from the modified scripts) are correct and intentional, he or she can run `ddrun -a` in the modified state. This will produce:

```
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
hello.py: nothing to accept
sorting.ipynb: nothing to accept
sorting.py: nothing to accept
```

---

To explore the DDD workflow, you can walk through these folders and see how demo scripts evolve, how differences are detected, how outputs are reverted or accepted.
