from __future__ import annotations


class Agent:
    pass

    # lst_prices : a list of dictionaries - each element in the list is a time_step, the dictionary maps from an agent to a float (price)
    # prior_sales_for_agent : int for prior sales

    def get_price(
        self, historic_set_prices: list[dict[Agent, float]], prior_sales_for_agent: int
    ) -> float:
        pass
