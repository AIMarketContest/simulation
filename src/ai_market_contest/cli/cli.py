import argparse
import initsubcommand


def initialise_parser():
    parser = argparse.ArgumentParser(
        description="Utility to set up AI contest simulation."
    )
    subparsers = parser.add_subparsers()

    # create the parser for the init command
    initsubcommand.create_subparser(subparsers)
    return parser


def main():
    parser = initialise_parser()
    args = parser.parse_args()
    print(args)
    args.func(args.path)


if __name__ == "__main__":
    main()
