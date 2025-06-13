# Showcase: the conventional folder for demo-driven development

The `showcase/` directory is the conventional location for demo scripts in a Demo-Driven Development (DDD) project.

The term "showcase" comes from the idea of *show* cases, similar to how `tests/` holds test cases and `docs/` contains documentation.

The default folder for `ddrun` is `demo`. Other common names include `example`, `examples`, `usage`, `tutorial`, and `guide`.

## Running the showcase

To run all demos in this folder:

```sh
ddrun -d showcase
ddrun
```

The result will be:

```
demo.sh: output matches saved result
nested.sh: output matches saved result
option_d.sh: output matches saved result
```

## Contents

### `demo.sh`

  Automates the typical DDD workflow in `showcase/demo/`.

  For details, see [showcase/demo/README.md](demo/README.md).

### `nested.sh`

  Demonstrates nested script calls.

  This script calls `showcase/nested1/nested.sh`, which in turn calls `showcase/nested2/nested.sh`, and finally invokes `showcase/option_d.sh`.

### `option_d.sh`

  Runs a variety of `ddrun -d` use cases.

### `demo/`

  Contains example scripts and output snapshots that demonstrate a typical Demo-Driven Development (DDD) workflow.

  See [showcase/demo/README.md](demo/README.md) for step-by-step instructions.

### `nested1/`, `nested2/`

  Support the nested script example. These directories validate deep nesting and `.dddir` context propagation.

### `extension/`

  Shows how to extend `ddrun` via `ddrun.ini` with custom file handlers.

  See [showcase/extension/README.md](extension/README.md) for configuration and usage details.
