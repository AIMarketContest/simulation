

# Simulation [![build](https://app.travis-ci.com/AIMarketContest/simulation.svg?token=gKutmzkeDupPkJGdM7M3&branch=main)](https://app.travis-ci.com/github/AIMarketContest/simulation/branches)
AI contests for deep reinforcement learning bots in online markets

## Prerequisites
Dependencies can be found in the `pyproject.toml` file.
Poetry has been set up to install all dependencies in a virtual environment.

To make use of this you should:
1. Download [poetry](https://python-poetry.org/)
2. Run `poetry install` to first install all dependencies
3. Run `poetry shell` to enter the virtual environment with access to the
   dependencies

## Developer tools
### Styling
When in the poetry virtual environment, [black](https://black.readthedocs.io/en/stable/) should be available and can be run with `black .`.

Furthermore, it is advisable to set up a pre-commit hook with black by running the following in the poetry virtual environment:

`pre-commit install`.

