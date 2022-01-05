import pathlib
from typing import Final

from ai_market_contest.agents.fixed_agent_fifty import FixedAgentFifty
from ai_market_contest.agents.fixed_agent_random import FixedAgentRandom
from ai_market_contest.agents.q_agent import QAgent
from ai_market_contest.agents.random_agent import RandomAgent
from ai_market_contest.agents.sarsa_agent import SarsaAgent
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction
from ai_market_contest.demandfunctions.fixed_lowest_takes_all_demand_function import (
    LowestTakesAllDemandFunction,
)
from ai_market_contest.demandfunctions.gaussian_demand_function import (
    GaussianDemandFunction,
)
from ai_market_contest.demandfunctions.noisy_fixed_demand_function import (
    NoisyFixedDemandFunction,
)

AGENT_TEMPLATE: Final = "agent.templ"
AGENT_PKL_FILENAME: Final = "agent.pkl"
AGENTS_DIR_NAME: Final = "agents"
DEMAND_FUNCTION_TEMPLATE = "demand_function.templ"
HASH_LENGTH: Final = 6
TRAINED_AGENTS_DIR_NAME: Final = "trained-agents"
META_FILENAME: Final = "metadata.ini"
COMMAND_NAME: Final = "ai-market-contest"
CLI_FILENAME: Final = "cli.py"
CLI_DIR: Final = pathlib.Path(__file__).parent
PROJ_DIR_NAME: Final = "aicontest"
CONFIG_FILENAME: Final = "config.ini"
ENVS_DIR_NAME: Final = "environments"
AGENT_FILENAME: Final = "agent.py"
DEMAND_FUNCTION_DIR_NAME: Final = f"{ENVS_DIR_NAME}/demandfunctions"
AGENT_FILE: Final = (CLI_DIR / ".." / AGENT_TEMPLATE).resolve()
DEMAND_FUNCTION_FILE: Final = (CLI_DIR / ".." / DEMAND_FUNCTION_TEMPLATE).resolve()
INITIAL_PICKLE_FILE_NAME: Final = "initial_pickle.pkl"
INITIAL_PICKLER_NAME: Final = "initial_pickler.py"
INITIAL_PICKLER_TEMPLATE: Final = "initial_pickler.templ"
INITIAL_PICKLER_FILE: Final = (CLI_DIR / ".." / INITIAL_PICKLER_TEMPLATE).resolve()
PICKLE_FILENAME: Final = "agent_pickle.pkl"
EXAMPLE_MAIN_FILENAME: Final = "example_main.py"
EXAMPLE_MAIN_FILE: Final = (CLI_DIR / ".." / EXAMPLE_MAIN_FILENAME).resolve()
ROOT_FOLDER: Final = (CLI_DIR / "..").resolve()
TRAIN_CONFIG_FILENAME: Final = "train_config.ini"
TRAINING_CONFIGS_DIR_NAME: Final = "training_configs"
TRAINING_CONFIG_FILE_EXTENSION: Final = ".ini"

RLLIB_AGENTS = [
    "AC2",
    "AC3",
    "BC",
    "DDPG",
    "TD3",
    "APEX-DDPG",
    "DQN",
    "Rainbow",
    "APEX-DQN",
    "IMPALA",
    "MARWIL",
    "PG",
    "PPO",
    "APPO",
    "R2D2",
    "SAC",
    "LinUCB",
    "LinTS",
    "QMIX",
    "MADDPG",
]

CUR_DEMAND_FUNCTIONS: Final = {
    "Fixed": FixedDemandFunction,
    "LowestTakesAll": LowestTakesAllDemandFunction,
    "Gaussian": GaussianDemandFunction,
    "NoisyFixed": NoisyFixedDemandFunction,
}

CUR_AGENTS: Final = {
    "QLearning": QAgent,
    "SARSA": SarsaAgent,
    "Random": RandomAgent,
    "FixedRandom": FixedAgentRandom,
    "FixedFifty": FixedAgentFifty,
}
