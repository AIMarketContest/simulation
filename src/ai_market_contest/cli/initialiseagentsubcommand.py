import pathlib
from typing import Any

def initialise_agent(args: Any):
    pass
    
def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser(
        "train", help="Initialise an agent for training"
    )
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=initialise_agent)