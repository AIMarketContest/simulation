from agents.q_agent import QAgent
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

simulation_length = 300
demand_function = LowestTakesAllDemandFunction()
env = Environment(simulation_length, demand_function)
q_agent1 = QAgent(env.action_space.n)

fixed_agent1 = FixedAgent(60)
fixed_agent2 = FixedAgent(70)
fixed_agent3 = FixedAgent(80)

env.add_agent(q_agent1)
env.add_agent(fixed_agent1)
env.add_agent(fixed_agent2)
env.add_agent(fixed_agent3)


reward_points = []
price_points = []

for x in trange(simulation_length):
    prices, rewards, _ = env.step()

    price_points.append(prices[0])
    reward_points.append(rewards[0])

plt.plot(list(range(simulation_length)), price_points, marker="o")
plt.plot(list(range(simulation_length)), reward_points, color="blue")

plt.show()
