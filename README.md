

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
If you wish to clone the project and manually install dependencies, giving you access to the code, you can follow the instructions in the [Contribution guide](docs/contributing.md).

# Running the program

Here is a brief overview of the toolbox's workflow:

<img src="docs/tutorial/aic_workflow.png" alt="Workflow">

A more in depth explanation and tutorial can be found [here](docs/tutorial/getting_started_tutorial.md).

## Developer tools

### Styling
When in the poetry virtual environment, [black](https://black.readthedocs.io/en/stable/) should be available and can be run with `black .`.

Furthermore, it is advisable to set up a pre-commit hook with black by running the following in the poetry virtual environment:

`pre-commit install`.

