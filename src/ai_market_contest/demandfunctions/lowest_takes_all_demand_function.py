from ai_market_contest.demand_function import DemandFunction


class LowestTakesAllDemandFunction(DemandFunction):
    def __init__(self, max_sales_scale_factor: int = 1000):
        self.max_sales_scale_factor = max_sales_scale_factor

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        sales: dict[str, int] = {agent: 0 for agent in current_prices.keys()}
        max_agents = []
        max_price = -1

        for agent, price in current_prices.items():
            if price == max_agents:
                max_agents.append(agent)
            elif price > max_price:
                max_agents = [agent]
                max_price = price

        for agent in max_agents:
            sales[agent] = int(self.max_sales_scale_factor / len(max_agents))

        return sales
