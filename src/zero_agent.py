class ZeroAgent:
    def get_initial_price(self) -> float:
        return 0

    def get_price(
        self,
        last_round_all_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> float:
        return 0
