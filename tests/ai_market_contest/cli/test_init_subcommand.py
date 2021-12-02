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

from cli_test_utils import check_is_agent, initialise_main_folder, run_cli_command


def test_init_creates_aicontest_folder_at_given_path(tmp_path, parser):
    # input for the program once it runs
    sys.stdin = io.StringIO("AgentName\nAuthor Name\n")
    run_cli_command(parser, ["init", str(tmp_path)])

    assert os.path.isdir(
        tmp_path / "aicontest"
    ), "aicontest folder either does not exist or is not a directory"


def test_can_specify_number_of_agents_to_initialise_with_using_n_flag(tmp_path, parser):
    agent_names = ["AgentMatteo", "AgentIbraheem", "AgentPranav"]

    sys.stdin = io.StringIO("\n".join(agent_names) + "\nAuthor Name\n")
    run_cli_command(parser, ["init", str(tmp_path), "-n", str(len(agent_names))])

    for agent_name in agent_names:
        check_is_agent(tmp_path, agent_name)


def test_default_number_of_agents_to_create_is_one(parser, tmp_path):
    agent_name = "AgentName"
    initialise_main_folder(parser, tmp_path, agent_name=agent_name)

    check_is_agent(tmp_path, agent_name)
