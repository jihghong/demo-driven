# Extension Showcase for ddrun

This directory demonstrates how to extend `ddrun` to support various file types through the `ddrun.ini` configuration file.

## Usage

1. Change the working directory to `showcase/extension`:

   ```bash
   cd showcase/extension
   ```

2. Set the demo directory explicitly using:

   ```bash
   ddrun -d ./
   ```

   or

   ```bash
   ddrun -d .
   ```

3. Run:

   ```bash
   ddrun
   ```

This will load the local `ddrun.ini` file and apply the custom file handlers defined for extensions such as `.sh`, `.bat`, `.ps1`, `.ast`, `.dis`, `.tok`, `.json`, `.yaml`, `.toml`, and `.csv`.

## Expected Output

If everything is set up correctly, you'll see results like:

```
demo.sh: output matches saved result
demo.bat: output matches saved result
demo.ps1: output matches saved result
demo.ast: output matches saved result
demo.dis: output matches saved result
demo.tok: output matches saved result
demo.json: output matches saved result
demo.yaml: output matches saved result
demo.toml: output matches saved result
demo.csv: output matches saved result
```

## Platform Notes

* **On Windows**:

  * To support `.sh` files, install one of the following:

    * [MSYS](https://www.msys2.org/)
    * [Cygwin](https://www.cygwin.com/)
    * [Git for Windows](https://git-scm.com/)
  * If none of the above are available, remove or comment out the `.sh` handler from `ddrun.ini`.

* **On Linux/Unix**:

  * You may want to remove or comment out the `.bat` and `.exe` handlers.
  * If PowerShell Core (`pwsh`) is not installed, remove the `.ps1` handler that uses it.

## About `ddrun.ini`

ddrun executes in the current working directory and reads the `ddrun.ini` file located there. For example, as described in the **Usage** section, after changing the working directory to `showcase/extension`, the command will read from `showcase/extension/ddrun.ini`.

To customize how `ddrun` processes files with specific extensions, define handlers in this configuration file.

### Tokens

Handler commands may need to refer to the file being processed or to the Python interpreter. To support this, `ddrun.ini` allows you to use special placeholders known as **tokens**, which will be replaced automatically at runtime:

* `{path}`: the path to the file being executed
* `{python}`: the path to the Python interpreter

### Built-in Handlers

The following handlers are built into `ddrun` by default:

```ini
py = {python} {path}
ipynb = {python} -m demo_driven.ddnb {path}
```

These definitions are equivalent to including them in your `ddrun.ini`. You may also override them with your own custom behavior.

### Path Syntax

When writing Windows paths in `ddrun.ini`, you can use any of the following formats:

* Double quotes with double backslashes:

  ```ini
  exe = "C:\\msys64\\usr\\bin\\bash.exe" {path}
  ```
* Single quotes with single backslashes:

  ```ini
  exe = 'C:\cygwin64\bin\bash.exe' {path}
  ```
* Forward slashes inside either quote type:

  ```ini
  exe = "C:/Program Files/Git/bin/bash.exe" {path}
  ```

## Demo Extensions Explained

Each custom extension listed in `ddrun.ini` maps to a specific processing command. The following examples use Python utilities to demonstrate extension handling:

* `.sh`, `.bat`, `.ps1`, `.exe`: executes the file as a shell or executable script
* `.ast`: Python source file to be parsed and printed as an Abstract Syntax Tree (AST)
* `.dis`: Python source file to be disassembled into bytecode instructions
* `.tok`: Python source file to be tokenized into lexical components
* `.json`: JSON file to be pretty-printed and syntax-checked
* `.yaml`: YAML file to be parsed and printed as a Python data structure
* `.toml`: TOML file to be parsed and printed as a dictionary
* `.csv`: CSV file to be parsed and shown as Python lists, one per line

These handlers demonstrate `ddrun`'s flexibility in handling a variety of formats using `python -m` or `python -c` patterns. In practice, users can define or override any of these to suit their specific needs.
