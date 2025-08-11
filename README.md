# demo-driven

Demo-Driven Development made easy.

`demo-driven` is a lightweight CLI tool that encourages writing executable, verifiable demo scripts alongside your codebase. These demos serve as working examples, documentation, and regression test anchors, all in one place.

---

## Features

- Captures and stores printed output from demo scripts (`.py`), Jupyter notebooks (`.ipynb`), and bash scripts (`.sh`)
- Generates `.html` diffs when output results change
- Lets users decide whether to accept new output after reviewing differences
- Includes `ddnbo`, a tool for checking and fixing notebook outputs to match actual execution
- Includes `ddcov`, a tool for executing demo scripts and collecting code coverage information

---

## Installation

```
pip install git+https://github.com/jihghong/demo-driven
```

---

## Usage

### Run a demo

```
ddrun hello
```

This runs `demo/hello.py` or `demo/hello.ipynb` and compares the output against `demo/hello.py.txt` or `demo/hello.ipynb.txt`.

If the corresponding `.txt` file does not exist, it will be created with the current output.
If the output has changed since the last run:
- The old `.txt` file will be renamed to `.tx~` (e.g., `hello.py.tx~`)
- A visual diff will be generated and saved as `.html` for you to review in a browser

You can also use wildcards to specify demos, for example:

```
ddrun h?l*o
```

When both hello.py and hello.ipynb exist, but you only want to run one of them, you can include the file extension in the pattern:

```
ddrun h?l*o.ipynb
```


### Accept new output

```
ddrun -a hello
```

Accepts the current result and deletes `.tx~` and `.html` to mark it as reviewed.

### Run all demos

```
ddrun
```

### Accept all new outputs

```
ddrun -a
```

This will check all demos and either accept the new output or confirm that nothing needs to be accepted.

### Use a custom demo directory

```
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

```
ddnbo
```

This executes each notebook and compares the actual outputs with the ones stored in notebook cells. It will report which code cells mismatch:

```
hello.ipynb: [1] mismatched
sorting.ipynb: [2][3][4][5] mismatched
```

### Fix mismatched outputs or keep untouched

```
ddnbo -f
```

This re-executes each notebook to fix the mismatched outputs. If no output mismatch, the notebook is kept untouched.

```
hello.ipynb: outputs updated
sorting.ipynb: outputs updated
```

### Force update all outputs

```
ddnbo -F
```

This will forcefully execute all code cells and update outputs in every notebook.

---

## Coverage Collector

The `ddcov` command runs your demo scripts and collects code coverage information using the coverage.py library.

It helps you understand how much of your code is exercised by your demos.

### Run and collect coverage

The usage is similar to ddrun, and you can use the following commands.

```
ddcov -d
ddcov -d showcase
ddcov
ddcov h?l*o.ipynb
```

This will execute all matching demos and generate a `.coverage` file in the current directory.

### Coverage report

You can then use standard `coverage` tools to inspect summary results or generate html reports, such as:  

```
coverage report
coverage html
```

---

## Example Workflow

1. Write runnable demos in `demo/hello.py`, `demo/sorting.py`, and `demo/sorting.ipynb`
2. Run them with `ddrun hello`, `ddrun sorting`, or simply `ddrun` to run all demos
3. The printed output will be saved into `.txt` files (e.g., `demo/hello.py.txt`, `demo/sorting.ipynb.txt`)
4. If you modify your code and the output changes:
   - A `.tx~` file will preserve the previous result
   - An `.html` file will help visualize the differences

5. If the output changed because of an intentional update, accept the result using `ddrun -a hello` or `ddrun -a`
6. Re-run `ddrun` anytime to verify whether demo behavior remains stable
7. Use `ddnbo` to check or repair notebook outputs:
   - Run `ddnbo` to check for mismatches
   - Run `ddnbo -f` to fix only the notebooks with mismatched cells
   - Run `ddnbo -F` to force all outputs to be regenerated

For more examples, explore the [showcase/](showcase/) directory. It includes demo scripts created for this project, along with shell scripts that help automate common demo workflows.

---

## Philosophy

> **Write demo before code.**
> Before implementing anything, writing a demo helps clarify your intent, explore your interface, and give your implementation a clear direction.

> **Output serves as baseline.**
> Printed output reflects your program's behavior. By capturing and keeping it as reference, you create a stable baseline. Any unexpected change in the output may reveal a mistake.

> **Evolve with minimal overhead.**
> When you change your program's logic, it is simpler and faster to move forward by reviewing the new output and accepting it, rather than maintaining and rewriting a forest of assertion code.

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

While TDD excels in enforcing correctness through assertions, it can become burdensome as the number of test cases grows. When logic changes, test files often need to be manually rewritten to reflect new expectations. This leads to significant friction and a fear of refactoring.

DDD offers a lighter-weight alternative. You capture behavior by example, and decide whether to accept changes after visually reviewing HTML diffs. This allows more fluid evolution of code, especially in early-stage or rapidly changing systems.

---

## License

MIT

---

## Authors

- **John Lin** – [jihghong@gmail.com](mailto:jihghong@gmail.com)
- **ChatGPT 4o** – Assistant co-author
