import argparse
import sys

import ai_market_contest.cli.addagentsubcommand as addagentsubcommand  # type: ignore
import ai_market_contest.cli.initsubcommand as initsubcommand  # type: ignore
import ai_market_contest.cli.resetsubcommand as resetsubcommand  # type: ignore
import ai_market_contest.cli.trainsubcommand as trainsubcommand  # type: ignore
import ai_market_contest.cli.runsubcommand as runsubcommand  # type: ignore

KEYBOARD_INTERRUPT_MSG = "Operation aborted."


def initialise_parser():
    parser = argparse.ArgumentParser(
        description="Utility to set up AI contest simulation."
    )
    subparsers = parser.add_subparsers()
    initsubcommand.create_subparser(subparsers)
    resetsubcommand.create_subparser(subparsers)
    addagentsubcommand.create_subparser(subparsers)
    trainsubcommand.create_subparser(subparsers)
    runsubcommand.create_subparser(subparsers)

    return parser


def no_arguments(args):
    print("No arguments supplied. Make sure use the -h flag to see available options.")
    sys.exit(-1)


def main():
    parser = initialise_parser()
    parser.set_defaults(func=no_arguments)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()  # print new line
        print(KEYBOARD_INTERRUPT_MSG)
        sys.exit(0)
