import pathlib

from ai_market_contest.cli.utils.execute_training_routine import (
    set_up_and_execute_training_routine,
)
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.training.training_regime.training_regime import TrainingRegime


class ConcreteTrainingRegime(TrainingRegime):
    def __init__(
        self,
        training_config_name: str,
        project_dir: pathlib.Path,
        agent_version: ExistingAgentVersion,
        training_msg: str,
    ):
        self.training_config_name = training_config_name
        self.project_dir = project_dir
        self.agent_version = agent_version
        self.training_msg = training_msg

    def execute(self) -> None:
        set_up_and_execute_training_routine(
            self.training_config_name,
            self.project_dir,
            self.agent_version,
            self.training_msg,
        )
