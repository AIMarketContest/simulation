import io
import os
import sys


def run_cli_command(parser, list_of_arguments):
    # parse arguments
    args = parser.parse_args(list_of_arguments)

    args.func(args)


def initialise_main_folder(
    parser, path, agent_name="AgentName", author_name="Author Name"
):
    # input for the program once it runs
    sys.stdin = io.StringIO(f"{agent_name}\n{author_name}\n")

    run_cli_command(parser, ["init", str(path)])


def check_is_agent(path_to_project, agent_name):
    # define project root directory
    agent_path = path_to_project / "aicontest" / "agents"

    agent_files = os.listdir(agent_path)

    # checks a directory with the agent name exists and is a directory
    assert (
        agent_name in agent_files
    ), f"Agent named '{agent_name}' does not have a directory"
    assert os.path.isdir(
        agent_path / agent_name
    ), f"Agent named '{agent_name}' is not represented as a directory"

    # checks that the agent file is within the directory
    assert os.path.isfile(agent_path / agent_name / f"{agent_name}.py"), (
        f"Directory of Agent named '{agent_name}' does not have a template",
    )
