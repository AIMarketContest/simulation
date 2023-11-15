import pathlib

from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.training.training_regime.concrete_training_regime import (
    ConcreteTrainingRegime,
)
from ai_market_contest.training.training_regime.training_regime import TrainingRegime


class TrainingRegimeFactory:
    @staticmethod
    def create_training_regime(
        training_config_name: str,
        project_dir: pathlib.Path,
        agent_version: ExistingAgentVersion,
        training_msg: str,
    ) -> TrainingRegime:
        return ConcreteTrainingRegime(
            training_config_name, project_dir, agent_version, training_msg
        )
