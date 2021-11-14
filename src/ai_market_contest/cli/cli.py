import argparse

import cli.addagentsubcommand
import cli.initsubcommand
import cli.resetsubcommand


def initialise_parser():
    parser = argparse.ArgumentParser(
        description="Utility to set up AI contest simulation."
    )
    subparsers = parser.add_subparsers()

    cli.initsubcommand.create_subparser(subparsers)
    cli.resetsubcommand.create_subparser(subparsers)
    cli.addagentsubcommand.create_subparser(subparsers)
    return parser


def main():
    parser = initialise_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
