# Localnet

This project has been generated using AlgoKit. See below for default getting started instructions.

# Setup

Open project folders individually

```sh
cd smart-contracts/master-beaker/localnet
```

Then setup your development environment with:

```sh
algokit bootstrap all
source .venv/bin/activate
```

Then run deploy scripts like:

```sh
cd beaker-calc
python3 localnet.py
```

### Subsequently

1. If you update to the latest source code and there are new dependencies you will need to run `poetry install` again
2. Follow step 3 above

# Tools

This project makes use of Python to build Algorand smart contracts. The following tools are in use:

- [Poetry](https://python-poetry.org/): Python packaging and dependency management.- [Black](https://github.com/psf/black): A Python code formatter.
- [Ruff](https://github.com/charliermarsh/ruff): An extremely fast Python linter.

- [mypy](https://mypy-lang.org/): Static type checker.

It has also been configured to have a productive dev experience out of the box in VS Code, see the [.vscode](./.vscode) folder.
