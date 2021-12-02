import argparse
import sys

import aimc.addagentsubcommand as addagentsubcommand  # type: ignore
import aimc.initialiseagentsubcommand as initialiseagentsubcommand  # type: ignore
import aimc.initsubcommand as initsubcommand  # type: ignore
import aimc.resetsubcommand as resetsubcommand  # type: ignore
import aimc.trainsubcommand as trainsubcommand  # type: ignore

import ai_market_contest.cli as aimc  # noqa: F401

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
    initialiseagentsubcommand.create_subparser(subparsers)
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
