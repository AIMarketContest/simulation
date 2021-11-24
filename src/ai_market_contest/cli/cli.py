﻿import argparse
import sys

import ai_market_contest.cli.addagentsubcommand as addagentsubcommand  # type: ignore
import ai_market_contest.cli.initsubcommand as initsubcommand  # type: ignore
import ai_market_contest.cli.resetsubcommand as resetsubcommand  # type: ignore
import ai_market_contest.cli.trainsubcommand as trainsubcommand  # type: ignore
import ai_market_contest.cli.initialiseagentsubcommand as initialiseagentsubcommand  # type: ignore

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


def main():
    parser = initialise_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()  # print new line
        print(KEYBOARD_INTERRUPT_MSG)
        sys.exit(0)
