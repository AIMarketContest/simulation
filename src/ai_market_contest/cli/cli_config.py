import pathlib
from typing import Final

AGENT_TEMPLATE: Final = "agent.templ"
AGENT_PKL_FILENAME: Final = "agent.pkl"
HASH_LENGTH: Final = 6
TRAINED_AGENTS_DIR_NAME: Final = "trained-agents"
META_FILENAME: Final = "metadata.ini"
COMMAND_NAME: Final = "ai-market-contest"
CLI_FILENAME: Final = "cli.py"
CLI_DIR: Final = pathlib.Path(__file__).parent
PROJ_DIR_NAME: Final = "aicontest"
CONFIG_FILENAME: Final = "config.ini"
AGENT_FILENAME: Final = "agent.py"
AGENTS_DIR_NAME: Final = "agents"
AGENT_FILE: Final = (CLI_DIR / ".." / AGENT_TEMPLATE).resolve()
INITIAL_PICKLE_FILE_NAME: Final = "initial_pickle.pkl"
INITIAL_PICKLER_NAME: Final = "initial_pickler.py"
INITIAL_PICKLER_TEMPLATE: Final = "initial_pickler.templ"
INITIAL_PICKLER_FILE: Final = (CLI_DIR / ".." / INITIAL_PICKLER_TEMPLATE).resolve()
PICKLE_FILENAME: Final = "agent_pickle.pkl"
EXAMPLE_MAIN_FILENAME: Final = "example_main.py"
EXAMPLE_MAIN_FILE: Final = (CLI_DIR / ".." / EXAMPLE_MAIN_FILENAME).resolve()
ENVS_DIR_NAME: Final = "environments"
ROOT_FOLDER: Final = (CLI_DIR / "..").resolve()
TRAIN_CONFIG_FILENAME: Final = "train_config.ini"
TRAINING_CONFIGS_DIR_NAME: Final = "training_configs"
