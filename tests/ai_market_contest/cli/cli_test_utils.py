import io
import os
import sys


def initialise_main_folder(
    parser, path, agent_name="AgentName", author_name="Author Name"
):
    # parse arguments
    args = parser.parse_args(["init", str(path)])

    # input for the program once it runs
    sys.stdin = io.StringIO(f"{agent_name}\n{author_name}\n")
    args.func(args)


def check_is_agent(path_to_project, agent_name):
    # define project root directory
    path = path_to_project / "aicontest"

    agent_files = os.listdir(path)

    # checks a directory with the agent name exists and is a directory
    assert (
        agent_name in agent_files
    ), f"Agent named '{agent_name}' does not have a directory"
    assert os.path.isdir(
        path / agent_name
    ), f"Agent named '{agent_name}' is not represented as a directory"

    # checks that the agent file is within the directory
    assert os.path.isfile(path / agent_name / f"{agent_name}.py"), (
        f"Directory of Agent named '{agent_name}' does not have a template",
    )
