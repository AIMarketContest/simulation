import pathlib
import pickle


def get_multi_agent_config(multi_agent_config_file: pathlib.Path):
    with multi_agent_config_file.open("rb") as config_file:
        multi_agent_config = pickle.load(config_file)
    return multi_agent_config
