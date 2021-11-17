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

    assert os.path.isdir(
        tmp_path / "aicontest"
    ), "aicontest folder either does not exist or is not a directory"


def test_can_specify_number_of_agents_to_initialise_with_using_n_flag(
    tmp_path, parser
):
    agent_names = ["AgentMatteo", "AgentIbraheem", "AgentPranav"]

    # parse arguments
    args = parser.parse_args(
        ["init", str(tmp_path), "-n", str(len(agent_names))]
    )

    sys.stdin = io.StringIO("\n".join(agent_names) + "\nAuthor Name\n")
    args.func(args)

    agent_files = os.listdir(tmp_path / "aicontest")

    for agent_name in agent_names:
        # checks a directory with the agent name exists and is a directory
        assert agent_name in agent_files, "given agent name does not exist"
        assert os.path.isdir(
            tmp_path / "aicontest" / agent_name
        ), "given agent is not represented as a folder"

        # checks that the agent file is within the directory
        assert os.path.isfile(
            tmp_path / "aicontest" / agent_name / f"{agent_name}.py"
        ), "agent folder does not have a template for the user"


def test_default_number_of_agents_to_create_is_one(parser, tmp_path):
    # parse arguments
    args = parser.parse_args(["init", str(tmp_path)])

    agent_name = "AgentName"
    # input for the program once it runs with only one agent
    sys.stdin = io.StringIO(f"{agent_name}\nAuthor Name\n")
    args.func(args)

    # checks a directory with the agent name exists and is a directory
    assert agent_name in os.listdir(
        tmp_path / "aicontest"
    ), "given agent name is not in the folder structure"
    assert os.path.isdir(
        tmp_path / "aicontest" / agent_name
    ), "given agent not represented as a folder"

    # checks that the agent file is within the directory
    assert os.path.isfile(
        tmp_path / "aicontest" / agent_name / f"{agent_name}.py"
    ), "agent folder does not have a template for the user"


def test_will_copy_example_usage_with_include_example_tag(parser, tmp_path):
    # parse arguments
    args = parser.parse_args(["init", str(tmp_path), "--include-example"])

    # input for the program once it runs
    sys.stdin = io.StringIO("AgentName\nAuthor Name\n")
    args.func(args)

    assert os.path.isfile(tmp_path / "aicontest/example_main.py")
