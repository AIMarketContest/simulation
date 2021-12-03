from typing import List

from ai_market_contest.environment import Environment


def agent_dict_to_list(agent_dict: dict[str, int], env: Environment) -> List[int]:
    agent_values: List[int] = []
    for agent_name in env.possible_agents:
        if agent_name in agent_dict:
            agent_values.append(agent_dict[agent_name])
        else:
            raise ValueError(f"Agent {agent_name} not found in agent_dict")
    return agent_values


def train(env):
    agent_sales = {agent_name: 0 for agent_name in env.possible_agents}
    previous_prices = {agent: 0 for agent in env.possible_agents}
    current_prices = {agent: 0 for agent in env.possible_agents}

    dones = {agent: False for agent in env.possible_agents}
    while all(dones.values()):
        print(previous_prices)
        _, rewards, dones, _ = env.step(previous_prices)
        for agent_name, reward in rewards.items():
            agent_sales[agent_name] += reward

        previous_prices_list = agent_dict_to_list(previous_prices, env)

        for index, agent_name in enumerate(env.possible_agents):
            current_prices[agent_name] = env.agent_name_mapping[agent_name].policy(
                previous_prices_list, index
            )

        current_prices_list = agent_dict_to_list(current_prices, env)
        for index, agent_name in enumerate(env.possible_agents):
            env.agent_name_mapping[agent_name].update(
                previous_prices_list,
                rewards[agent_name],
                current_prices_list,
                index,
            )

        previous_prices = current_prices
