# Contribute to this project #
:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to AIMarketContest and its packages, which are hosted in the [AIMarketContest Organization](https://github.com/AIMarketContest) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.
This document should outline how to get set up for developing this project, and the steps to take to propose a contribution or report a bug.

## Setup ##
You should start by forking the repository using the button on Github. You can then clone the repository to your local machine:
```
git clone git@github.com:your-username/simulation.git
```

Dependencies can be found in the `pyproject.toml` file in the root of the cloned project.
Poetry is used to install all dependencies in a virtual environment.

To make use of this you should:
1. Download [poetry](https://python-poetry.org/)
2. Run `poetry install` to first install all dependencies
3. Run `poetry shell` to enter the virtual environment with access to the dependencies

We recommend setting up an alias and running all commands from the root directory as follows:
```
alias aic="python3 src/ai_market_contest/cli/aic.py"
```

## Reporting Bugs ##
We are happy to help you fix any bugs you find but we ask you to do the following before submitting the issue:
- check [open issues](https://github.com/AIMarketContest/simulation/issues) to make sure the bug hasn't been reported before
- check [closed issues](https://github.com/AIMarketContest/simulation/issues?q=is%3Aissue+is%3Aclosed) to check if this issue has been resolved before
- give a reproducible example of the bug when filing out the issue

We also welcome suggestions on new features, however, we ask that you are respectful to the contributors as this is a hobby project.

## Pull Requests ##
We encourage you to try implementing new features and fixing any bugs in the library. Once you have done this locally you can contribute back to the library by using a pull request. To maintain the quality of the code we would like you to ensure that you do the following:
- Make sure that all existing tests pass with your new changes
- Make sure you have added exhaustive test cases for your new changes
- Format your code using the `black` formatter (run `black .` in the project root)
- Sort import using `isort` (run `isort .` in the project root)

On submission of the pull request, the automated CI pipeline will run to check the styling and testing of the PR. Once this is passing we will review the changes and merge the PR into main!

We look forward to seeing your contributions to the repository!
