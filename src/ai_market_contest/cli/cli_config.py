import pathlib

AGENT_TEMPLATE: str = "agent.templ"
AGENT_PKL_FILENAME = "agent.pkl"
HASH_LENGTH: int = 6
TRAINED_AGENTS_DIR_NAME = "trained-agents"
META_FILENAME: str = "metadata.ini"
COMMAND_NAME: str = "ai-market-contest"
CLI_FILENAME: str = "cli.py"
CLI_DIR: pathlib.Path = pathlib.Path(__file__).parent
PROJ_DIR_NAME: str = "aicontest"
CONFIG_FILENAME: str = "config.ini"
AGENT_FILENAME: str = "agent.py"
AGENTS_DIR_NAME: str = "agents"
AGENT_FILE: pathlib.Path = (CLI_DIR / ".." / AGENT_TEMPLATE).resolve()
INITIAL_PICKLE_FILE_NAME = "initial_pickle.pkl"
INITIAL_PICKLER_NAME = "initial_pickler.py"
INITIAL_PICKLER_TEMPLATE = "initial_pickler.templ"
INITIAL_PICKLER_FILE = (CLI_DIR / ".." / INITIAL_PICKLER_TEMPLATE).resolve()
PICKLE_FILENAME = "agent_pickle.pkl"
EXAMPLE_MAIN_FILENAME: str = "example_main.py"
EXAMPLE_MAIN_FILE: pathlib.Path = (CLI_DIR / ".." / EXAMPLE_MAIN_FILENAME).resolve()
ENVS_DIR_NAME: str = "environments"
ROOT_FOLDER: pathlib.Path = (CLI_DIR / "..").resolve()
TRAIN_CONFIG_FILENAME: str = "train_config.ini"
TRAINING_CONFIGS_DIR_NAME: str = "training_configs"
