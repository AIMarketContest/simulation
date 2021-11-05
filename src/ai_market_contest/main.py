﻿from agents.q_agent import QAgent
from agents.fixed_agent import FixedAgent
from demandfunctions.gaussian_demand_function import GaussianDemandFunction
from demandfunctions.fixed_demand_function import FixedDemandFunction
from demandfunctions.lowest_takes_all_demand_function import (
    LowestTakesAllDemandFunction,
)
from demandfunctions.noisy_fixed_demand_function import NoisyFixedDemandFunction
from environment import Environment
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import trange

mpl.use("TkAgg")
plt.style.use("ggplot")

<<<<<<< HEAD:src/ai_market_contest/main.py
simulation_length = 300
demand_function = LowestTakesAllDemandFunction()
env = Environment(simulation_length, demand_function)
q_agent1 = QAgent(env.action_space.n)
=======
simulation_length = 15000
demand_function = LowestTakesAllDemandFunction()
env = Environment(simulation_length, demand_function)
q_agent1 = QAgent(env.action_space.n)
# q_agent2 = QAgent(env.action_space.n)

# sarsa_agent = SarsaAgent(env.action_space.n)
>>>>>>> 1ddf931 (Fix formatting):src/main.py

fixed_agent1 = FixedAgent(60)
# fixed_agent2 = FixedAgent(70)
# fixed_agent3 = FixedAgent(80)

env.add_agent(q_agent1)
<<<<<<< HEAD:src/ai_market_contest/main.py
env.add_agent(fixed_agent1)
env.add_agent(fixed_agent2)
env.add_agent(fixed_agent3)
=======
# env.add_agent(sarsa_agent)
# env.add_agent(q_agent2)
env.add_agent(fixed_agent1)
# env.add_agent(fixed_agent2)
# env.add_agent(fixed_agent3)
>>>>>>> 1ddf931 (Fix formatting):src/main.py


reward_points = []
price_points = []

for x in trange(simulation_length):
    prices, rewards, _ = env.step()

    price_points.append(prices[0])
    reward_points.append(rewards[0])

<<<<<<< HEAD:src/ai_market_contest/main.py
plt.plot(list(range(simulation_length)), price_points, marker="o")
plt.plot(list(range(simulation_length)), reward_points, color="blue")
=======
plt.plot(
    list(range(len(price_points_agent1))), price_points_agent1, marker="o", color="blue"
)
plt.plot(list(range(len(price_points_agent2))), price_points_agent2, color="red")
# plt.plot(list(range(len(price_points))), reward_points, color="blue")
>>>>>>> 1ddf931 (Fix formatting):src/main.py

plt.show()
