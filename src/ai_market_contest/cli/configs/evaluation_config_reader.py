from ai_market_contest.cli.configs.simulation_config_reader import (
    SimulationConfigReader,
)


class EvaluationConfigReader(SimulationConfigReader):
    def get_num_agents(self) -> int:
        return sum(self.get_naive_agent_counts().values())
