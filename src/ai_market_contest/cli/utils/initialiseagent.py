import datetime
import pathlib
import shutil

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENT_FILE,
    ABS_METHOD_STR,
    IMPORT_STR,
    AGENT_STR,
    CLASS_METHOD_STR,
    TRAINED_AGENTS_DIR_NAME,
    INITIAL_PICKLER_FILE,
    INITIAL_PICKLER_NAME,
)
from ai_market_contest.cli.utils.processmetafile import write_meta_file


def make_initial_trained_agent(agent_dir: pathlib.Path, initial_hash: str):
    trained_agents_dir = agent_dir / TRAINED_AGENTS_DIR_NAME
    initial_trained_agent_dir = trained_agents_dir / initial_hash
    initial_trained_agent_dir.mkdir(parents=True)
    msg = "Initial untrained agent"
    write_meta_file(
        initial_trained_agent_dir, initial_hash, datetime.datetime.now(), msg
    )

    shutil.copy(INITIAL_PICKLER_FILE, agent_dir / INITIAL_PICKLER_NAME)


def make_agent_classname_camelcase(agent_name: str):
    AGENT_STR = "agent"
    if AGENT_STR.capitalize() in agent_name:
        return agent_name
    agent_name_cc = agent_name.lower()
    if AGENT_STR in agent_name_cc:
        agent_name_cc = agent_name_cc.replace(AGENT_STR, AGENT_STR.capitalize())
    return agent_name_cc[0].upper() + agent_name_cc[1:]


def create_new_agent_file(agent_file: pathlib.Path, agent_name: str):
    class_line_tab: bool = False
    with agent_file.open("w") as f1:
        f1.write("from ai_market_contest.agent import Agent\n")
        with AGENT_FILE.open("r") as f2:
            for line in f2:
                if line is not None:
                    if CLASS_METHOD_STR in line:
                        break
                    if IMPORT_STR in line:
                        continue
                    if ABS_METHOD_STR in line:
                        continue
                    if AGENT_STR in line:
                        tab = "\t" if class_line_tab else ""
                        f1.write(
                            tab
                            + "class "
                            + make_agent_classname_camelcase(agent_name)
                            + "(Agent):\n"
                        )
                        class_line_tab = True
                    else:
                        f1.write(line)
