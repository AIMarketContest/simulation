import random


class RandomAgent:
    """
    This agent is a testing agent used to run the simulation.
    The agent returns a random price between 0 and 1 everytime its get_price method is called
    """
    def get_initial_price(self) -> float:
        return 0

    def get_price(
            self,
            last_round_all_agents_prices: list[float],
            last_round_sales: int,
            identity_index: int,
    ) -> float:
        return random.random()
