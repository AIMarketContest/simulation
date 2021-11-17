import io
import sys


def initialise_main_folder(
    parser, path, agent_name="AgentName", author_name="Author Name"
):
    # parse arguments
    args = parser.parse_args(["init", str(path)])

    # input for the program once it runs
    sys.stdin = io.StringIO(f"{agent_name}\n{author_name}\n")
    args.func(args)
