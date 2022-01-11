from ai_market_contest.demand_function import DemandFunction


class LowestTakesAllDemandFunction(DemandFunction):
    MAX_SALES_SCALE_FACTOR: int = 1000

    def __init__(self):
        pass

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        sales: dict[str, int] = {agent: 0 for agent in current_prices.keys()}
        min_agents = []
        min_price = float("inf")

        for agent, price in current_prices.items():
            if price == min_price:
                min_agents.append(agent)
            elif price < min_price:
                min_agents = [agent]
                min_price = price

        agent_sales = int(self.MAX_SALES_SCALE_FACTOR / len(min_agents))
        for agent in min_agents:
            sales[agent] = agent_sales

        return sales
