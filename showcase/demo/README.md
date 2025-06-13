# Demo Walkthrough

This folder demonstrates the Demo-Driven Development (DDD) workflow using example demo scripts and their corresponding outputs.

### Initial state

The folder `showcase/demo/current` contains the original demo scripts: `hello.py`, `hello.ipynb`, `sorting.py`, and `sorting.ipynb`.

As the first step, run `ddrun -d showcase/demo/current` to set the target directory. This will write a `.dddir` file to remember the setting for both `ddrun` and `ddnbo`.

### Establishing the initial baseline

Now run `ddrun` to execute all the demo scripts in the folder. You will see output like:

```
hello.ipynb: output saved
hello.py: output saved
sorting.ipynb: output saved
sorting.py: output saved
```

The outputs of the demo scripts are captured and saved as the initial baseline. As a result, the directory now becomes like the contents of `showcase/demo/created/`.

If you run `ddrun` again in this state, you will see:

```
hello.ipynb: output matches saved result
hello.py: output matches saved result
sorting.ipynb: output matches saved result
sorting.py: output matches saved result
```

This represents the initial output being locked in as the behavioral baseline.

### Making changes to the code

Suppose the author modifies the demo scripts into the versions found in `showcase/demo/modified/hello.py`, `showcase/demo/modified/hello.ipynb`, `showcase/demo/modified/sorting.py`, and `showcase/demo/modified/sorting.ipynb`.

If you run `ddrun` in this state, you will see:

```
hello.ipynb: output changed, see hello.ipynb.html
hello.py: output changed, see hello.py.html
sorting.ipynb: output changed, see sorting.ipynb.html
sorting.py: output changed, see sorting.py.html
```

The output of each script is updated in `*.txt`, while the previous baseline is preserved as `.old` files. You can open the corresponding `.html` files to visually inspect the differences.

At this point, the directory becomes like the contents of `showcase/demo/modified/`.

### Reverting to output-compatible code

After the author modified the scripts, suppose later he or she changes them again into the versions found in `showcase/reverted/hello.py`, `showcase/reverted/hello.ipynb`, `showcase/reverted/sorting.py` and `showcase/reverted/sorting.ipynb`.

Although the code might be different from the original, the output matches the original baseline.

If you run `ddrun` in this state, you will see:

```
hello.ipynb: output matches saved result
hello.py: output matches saved result
sorting.ipynb: output matches saved result
sorting.py: output matches saved result
```

Regardless of code changes, identical output is treated as a reversion to the original behavior. `.old` and `.html` files are automatically deleted upon detecting the match.

As a result, the directory now becomes like the contents of `showcase/demo/reverted/`.

### Accepting the new behavior as baseline

If the author decides that the new outputs produced by `showcase/demo/modified/hello.py`, `showcase/demo/modified/hello.ipynb`, `showcase/demo/modified/sorting.py`, and `showcase/demo/modified/sorting.ipynb` are correct and intentional, he or she can run `ddrun -a` to accept them. This will produce:

```
hello.ipynb: accepted
hello.py: accepted
sorting.ipynb: accepted
sorting.py: accepted
```

The changes are confirmed and accepted. `.txt` files are updated with the new output. `.old` and `.html` files are automatically deleted. This represents a new stable state where updated behavior is locked in.

If you run `ddrun -a` again after accepting, you will see:

```
hello.ipynb: nothing to accept
hello.py: nothing to accept
sorting.ipynb: nothing to accept
sorting.py: nothing to accept
```

At this point, the directory becomes like the contents of `showcase/demo/accepted/`.

### Fixing notebook outputs

Notebook outputs can be refreshed using the `ddnbo` tool. `ddnbo` stands for **Demo-Driven Notebook Output** fixer.

For example, `hello.ipynb` has correct code but incorrect outputs stored in its cells. `sorting.ipynb` hasn't been executed yet, so its cells are missing output altogether. You can use `ddnbo` to detect and fix both situations.

Since `ddnbo` also reads the `.dddir` setting, it will automatically continue using the same target directory `showcase/demo/current/` set earlier by `ddrun -d showcase/demo/current`. You can also use `ddnbo -d showcase/demo/current` to set it.

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

This process results in notebook files matching those in `showcase/demo/fixed/`.

### Automating the Walkthrough

To streamline the walkthrough, all of the above steps have been automated into the showcase/demo.sh script. You can run:

```
ddrun -d showcase
ddrun demo
```

This will execute the `demo.sh` script inside `showcase/`. If `ddrun demo` seems to be unresponsive, you can observe the continuous changes in the files under `showcase/demo/current` to confirm that execution is actively progressing. When complete, you should see a summary line like:

```
demo.sh: output matches saved result
```
