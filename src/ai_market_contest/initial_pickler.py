import pickle

# from <agent_filename> import <agent_classname>

from ai_market_contest.cli.cli_config import (
    INITIAL_PICKLER_FILE,
    INITIAL_PICKLE_FILE_NAME,
)

# agent = <agent_classname>(<parameters>)

pickle_file = (INITIAL_PICKLER_FILE.parent) / INITIAL_PICKLE_FILE_NAME

with pickle_file.open("wb") as pkl:
    pickle.dump(agent, pkl)
