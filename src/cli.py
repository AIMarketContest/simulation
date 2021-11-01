import argparse
import pathlib
import os
import shutil


def initialise_file_structure(path):
    if not path.is_dir():
        raise IllegalArgumentError
    os.mkdir(path / "aicontest")
    shutil.copyfile("agent.py", path / "aicontest" / "agent.py")


def initialise_parser():
    parser = argparse.ArgumentParser(
        description="Utility to set up AI contest simulation."
    )
    subparsers = parser.add_subparsers()

    # create the parser for the init command
    parser_init = subparsers.add_parser(
        "init", help="Initialises a folder structure for a project"
    )
    parser_init.add_argument(
        "path",
        type=pathlib.Path,
        default=".",
    )
    parser_init.set_defaults(func=initialise_file_structure)
    return parser


def main():
    parser = initialise_parser()
    args = parser.parse_args()
    print(args)
    args.func(args.path)


if __name__ == "__main__":
    main()
