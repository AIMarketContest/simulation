import pathlib

CLI_FILENAME = "cli.py"
CLI_DIR = pathlib.Path(__file__).parent
PROJ_DIR_NAME = "aicontest"
CONFIG_FILENAME = "config.ini"
AGENT_FILENAME = "agent.py"
AGENT_FILE = (CLI_DIR / ".." / AGENT_FILENAME).resolve()
EXAMPLE_MAIN_FILENAME = "example_main.py"
EXAMPLE_MAIN_FILE = (CLI_DIR / ".." / EXAMPLE_MAIN_FILENAME).resolve()
