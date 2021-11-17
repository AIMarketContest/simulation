"""
# Behaviour:
- Should create an aicontest folder at the given location
- Should take a -n flag specifying the number of agents to create at launch
- The -n flag should default to 1 agent
- The --include-example argument should include an example of running the
  program
"""

import io
import os
import os.path
import sys

import pytest
from cli import initialise_parser


@pytest.fixture
def parser():
    return initialise_parser()


def test_init_creates_aicontest_folder_at_given_path(tmp_path, parser):
    # parse arguments
    args = parser.parse_args(["init", str(tmp_path)])

    # input for the program once it runs
    sys.stdin = io.StringIO("AgentName\nAuthor Name\n")
    args.func(args)

    assert os.path.isdir(tmp_path / "aicontest")


def test_can_specify_number_of_agents_to_initialise_with_using_n_flag():
    raise NotImplementedError


def test_default_number_of_agents_to_create_is_one():
    raise NotImplementedError


def test_will_copy_example_usage_with_include_example_tag():
    raise NotImplementedError
