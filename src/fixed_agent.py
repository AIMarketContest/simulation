class FixedAgent:
    """
    This agent is a testing agent used to trial run the simulation.
    It returns a fixed price, which the user can set or 0.5 by default, every time get_price is called.
    """
    def __init__(self, price=0.5):
        if (0 > price) or (price > 1):
            price = 0.5
        self.price = price

    def get_initial_price(self) -> float:
        return self.price

    def get_price(
        self,
        last_round_all_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> float:
        return self.price