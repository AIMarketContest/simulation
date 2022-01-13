

# Simulation
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/AIMarketContest/simulation/branch/main/graph/badge.svg?token=T232TJMI22)](https://codecov.io/gh/AIMarketContest/simulation)

AI contests for deep reinforcement learning bots in online markets

## Install
You can install the package through [pip](https://pip.pypa.io/en/stable/) using 
```
pip install git+https://github.com/AIMarketContest/simulation.git
```

You will then interface with the package through the `aic` command.
## For devs
If you wish to clone the project and manually install dependencies, giving you access to the code, you can follow the instructions below. You may also be interested in contributing, so we encourage you to check out the [Contribution guide](docs/contributing.md)

Dependencies can be found in the `pyproject.toml` file.
Poetry is used to install all dependencies in a virtual environment.

To make use of this you should:
1. Download [poetry](https://python-poetry.org/)
2. Run `poetry install` to first install all dependencies
3. Run `poetry shell` to enter the virtual environment with access to the
   dependencies

We recommend setting up an alias and running all commands from the root directory as follows:
```
alias aic="python3 src/ai_market_contest/cli/aic.py"
```

# Running the program

Here is a brief overview of the toolbox's workflow:

<img src="docs/tutorial/aic_workflow.png" alt="Workflow">

A more in depth explanation and tutorial can be found [here](docs/tutorial/getting_started_tutorial.md).

## Developer tools

### Styling
When in the poetry virtual environment, [black](https://black.readthedocs.io/en/stable/) should be available and can be run with `black .`.

Furthermore, it is advisable to set up a pre-commit hook with black by running the following in the poetry virtual environment:

`pre-commit install`.

