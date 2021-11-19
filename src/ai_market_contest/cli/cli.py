import argparse

import ai_market_contest.cli.addagentsubcommand as addagentsubcommand  # type: ignore
import ai_market_contest.cli.initsubcommand as initsubcommand  # type: ignore
import ai_market_contest.cli.resetsubcommand as resetsubcommand  # type: ignore


def initialise_parser():
    parser = argparse.ArgumentParser(
        description="Utility to set up AI contest simulation."
    )
    subparsers = parser.add_subparsers()

    initsubcommand.create_subparser(subparsers)
    resetsubcommand.create_subparser(subparsers)
    addagentsubcommand.create_subparser(subparsers)
    return parser


def main():
    parser = initialise_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
