# demo-driven

Demo-Driven Development made easy.

`demo-driven` is a lightweight CLI tool that encourages writing executable, verifiable demo scripts alongside your codebase. These demos serve as working examples, documentation, and regression test anchors—all in one place.

---

## Features

- Captures and stores printed output from demo scripts (`.py`) and Jupyter notebooks (`.ipynb`)
- Lock in output results for future refactor safety
- Generates `.html` and `.txt.old` files when behavior changes
- Accept new behavior only when explicitly reviewed
- Drive development through exploratory demo scripts
- Persist preferred demo directory in `.dddir`
- Includes `ddnbo`, a tool for checking and fixing notebook outputs to match actual execution

---

## Installation

```bash
pip install demo-driven
```

---

## Usage

### Run a demo

```bash
ddrun hello
```

This runs `demo/hello.py` or `demo/hello.ipynb` and compares the output against `demo/hello.py.txt` or `demo/hello.ipynb.txt`.

If the corresponding `.txt` file does not exist, it will be created with the current output.
If the output has changed since the last run:
- The old `.txt` file will be renamed to `.txt.old` (e.g., `hello.py.txt.old`)
- A visual diff will be generated and saved as `.html` for you to review in a browser

### Accept new output

```bash
ddrun -a hello
```

Accepts the current result and deletes `.txt.old` and `.html` to mark it as reviewed.

### Run all demos

```bash
ddrun
```

### Accept all new outputs

```bash
ddrun -a
```

This will check all demos and either accept the new output or confirm that nothing needs to be accepted.

### Use a custom demo directory

```bash
ddrun -d examples
```

This will:
- Store `examples` in `.dddir` as the default demo directory

Future commands (like `ddrun hello`, `ddrun -a`, etc.) will use `examples/` as the working demo directory until changed.

---

## Notebook Output Checker

The `ddnbo` command (short for Demo-Driven Notebook Output) checks or updates output cells inside Jupyter notebooks.

If you have previously run `ddrun -d demo`, the same `.dddir` setting applies to `ddnbo`.

### Check notebook outputs

```bash
ddnbo
```

This executes each notebook and compares the actual outputs with the ones stored in notebook cells. It will report which code cells mismatch:

```
hello.ipynb: [1] mismatched
sorting.ipynb: [2][3][4][5] mismatched
```

### Fix mismatched outputs or keep untouched

```bash
ddnbo -f
```

This re-executes each notebook to fix the mismatched outputs. If no output mismatch, the notebook is kept untouched.

```
hello.ipynb: outputs updated
sorting.ipynb: outputs updated
```

### Force update all outputs

```bash
ddnbo -F
```

This will forcefully execute all code cells and update outputs in every notebook.

---

## Example Workflow

1. Write runnable demos in `demo/hello.py`, `demo/sorting.py`, and `demo/sorting.ipynb`
2. Run them with `ddrun hello`, `ddrun sorting`, or simply `ddrun` to run all demos
3. The printed output will be saved into `.txt` files (e.g., `demo/hello.py.txt`, `demo/sorting.ipynb.txt`)
4. If you modify your code and the output changes:
   - A `.txt.old` file will preserve the previous result
   - An `.html` file will help visualize the differences

5. If the output changed because of an intentional update, accept the result using `ddrun -a hello` or `ddrun -a`
6. Re-run `ddrun` anytime to verify whether demo behavior remains stable
7. Use `ddnbo` to check or repair notebook outputs:
   - Run `ddnbo` to check for mismatches
   - Run `ddnbo -f` to fix only the notebooks with mismatched cells
   - Run `ddnbo -F` to force all outputs to be regenerated

For a full real-world example, see the [demo/](demo/) subdirectory.

---

## Philosophy

> **Write your demo before your code.**  
> Use the demo to shape your interface, guide your implementation, and clarify your intent—before you write a single function.

> **Lock in behavior with output.**  
> When your program prints something, it reflects what it does. By capturing that output as a reference, you create a stable baseline. Any future difference means something changed—and that change deserves your attention.

### Comparison with Test-Driven Development

Demo-Driven Development (DDD) and Test-Driven Development (TDD) share a common philosophy:

- Both encourage writing something **before the code** to clarify intent.
- Both serve as **living documentation** and **regression protection**.
- Both help drive implementation through external expectations rather than internal assumptions.

The key difference lies in **what is written** and **how behavior is captured**:

| Aspect              | TDD                                      | DDD                                      |
|---------------------|-------------------------------------------|-------------------------------------------|
| Focus               | Assertions and invariants                 | Printed output and observable behavior    |
| Expression format   | `assert ... == ...`                       | `print(...)` and inspection               |
| Verification        | Automated via test framework              | Human-verified, visually reviewed         |
| Maintenance cost    | High: test logic must evolve with code    | Low: only accept updated output when needed |
| Ideal for           | Systems with stable, mature logic         | Systems still evolving, where behavior is in flux but output can be meaningfully reviewed  |

While TDD excels in enforcing correctness through assertions, it can become burdensome as the number of test cases grows. When logic changes, test files often need to be manually rewritten to reflect new expectations—leading to significant friction and a fear of refactoring.

DDD offers a lighter-weight alternative. You capture behavior by example, and decide whether to accept changes after visually reviewing HTML diffs. This allows more fluid evolution of code, especially in early-stage or rapidly changing systems.


## License

MIT

---

## Authors

- **John Lin** – [jihghong@gmail.com](mailto:jihghong@gmail.com)
- **ChatGPT 4o** – Assistant co-author
