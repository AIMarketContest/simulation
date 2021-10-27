# Simulation
AI contests for deep reinforcement learning bots in online markets

# Prerequisites
Dependencies can be found in the `pyproject.toml` file.
Poetry has been set up to install all dependencies in a virtual environment. To
make use of this you should:
1. download [poetry](https://python-poetry.org/)
1. run `poetry install` to first install all dependencies
1. run `poetry shell` to enter the virtual environment with access to the
   dependencies

# Developer tools
## Styling
When in the poetry virtual environment, [black](https://black.readthedocs.io/en/stable/) should be available and can be run
with `black .`.
Furthermore, it is advisable to set up a pre-commit hook with black by running
the following in the poetry virtual environment:
`pre-commit install`.

