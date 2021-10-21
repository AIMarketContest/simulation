from agent import Agent


class DemandFunction:
    pass

    def get_sales(self, set_prices: list[float]) -> list[int]:
        demand_list = []
        for _ in range(len(set_prices)):
            demand_list.append(1)
        return demand_list
