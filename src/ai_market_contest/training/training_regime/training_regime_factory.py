import pathlib

from ai_market_contest.cli.configs.agent_config_reader import AgentConfigReader
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.training.training_regime.custom_agent_training_regime import (
    CustomAgentTrainingRegime,
)
from ai_market_contest.training.training_regime.rllib_agent_training_regime import (
    RLLibAgentTrainingRegime,
)
from ai_market_contest.training.training_regime.training_regime import TrainingRegime


class TrainingRegimeFactory:
    @staticmethod
    def create_training_regime(
        training_config: TrainingConfigReader,
        project_dir: pathlib.Path,
        agent_version: ExistingAgentVersion,
        training_msg: str,
    ) -> TrainingRegime:
        agent_config_reader: AgentConfigReader = AgentConfigReader(agent_version)
        if agent_config_reader.get_agent_type() == "rllib":
            return RLLibAgentTrainingRegime(
                training_config,
                project_dir,
                agent_version,
                training_msg,
                agent_config_reader,
            )
        else:
            return CustomAgentTrainingRegime(
                training_config,
                project_dir,
                agent_version,
                training_msg,
                agent_config_reader,
            )
