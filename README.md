# demo-driven

Demo-Driven Development made easy.

`demo-driven` is a lightweight CLI tool that encourages writing executable, verifiable demo scripts alongside your codebase. These demos serve as working examples, documentation, and regression test anchors—all in one place.

---

## Features

- Captures and stores printed output from demo scripts
- Lock in output results for future refactor safety
- Generates `.html` and `.txt.old` files when behavior changes
- Accept new behavior only when explicitly reviewed
- Drive development through exploratory demo scripts

---

## Installation

```bash
pip install demo-driven
```

---

## Usage

### Run a demo

```bash
demo hello
```

This runs `demo/hello.py` and compares its output against `demo/hello.txt`.

If `demo/hello.txt` does not exist, it will be created with the current output.
If the output has changed since the last run:
- The old `hello.txt` will be renamed to `hello.txt.old`
- A visual diff will be generated and saved as `hello.html` for you to review in a browser

### Accept new output

```bash
demo -a hello
```

Accepts the current result and deletes `.txt.old` and `.html` to mark it as reviewed.

### Run all demos

```bash
demo -r
```

### Accept all new outputs

```bash
demo -a
```

This will check all demos and either accept the new output or confirm that nothing needs to be accepted.

---


## Example Workflow

1. Write your expected usage as runnable scripts in `demo/hello.py` and `demo/sorting.py`
2. Run them with `demo hello`, `demo sorting`, or `demo -r` to run all demos
3. The printed output will be saved into `demo/hello.txt` and `demo/sorting.txt`
4. If you later modify your code and the output differs from what's stored:
   - A `.txt.old` file will be created to preserve the previous result
   - An `.html` file will be generated to visualize the diff for review

   For example, if you accidentally break the logic in `demo/sorting.py`, repeated runs of `demo sorting` will keep warning that the output has changed, until you fix the bug and the output matches again. Once matched, `.txt.old` and `.html` will be automatically deleted.

5. If the output changed because you intentionally updated the logic, you can accept the new result after reviewing it:
   - Run `demo -a sorting` to accept the new output for the specified demo script
   - Or run `demo -a` to accept all updated outputs

6. When the demo results are confirmed, commit both `.py` and `.txt` files into version control. These `.txt` files serve as the reference for future comparisons.
   - Re-run all demos with `demo -r` to check whether any behavior has changed

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
| Ideal for           | Systems with mature logic where correctness must be preserved  | Systems still evolving, where behavior is in flux but output can be meaningfully reviewed  |

While TDD excels in enforcing correctness through assertions, it can become burdensome as the number of test cases grows. When logic changes, test files often need to be manually rewritten to reflect new expectations—leading to significant friction and a fear of refactoring.

DDD offers a lighter-weight alternative. You capture behavior by example, and decide whether to accept changes after visually reviewing HTML diffs. This allows more fluid evolution of code, especially in early-stage or rapidly changing systems.



## License

MIT

---

## Authors

- **John Lin** – [jihghong@gmail.com](mailto:jihghong@gmail.com)
- **ChatGPT 4o** – Assistant co-author
