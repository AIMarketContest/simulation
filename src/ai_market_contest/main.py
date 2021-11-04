from agents.q_agent import QAgent
from agents.fixed_agent import FixedAgent
from demandfunctions.gaussian_demand_function import GaussianDemandFunction
from demandfunctions.fixed_demand_function import FixedDemandFunction
from environment import Environment
import matplotlib.pyplot as plt
from tqdm import trange

plt.style.use("ggplot")
simulation_length = 100
demand_function = FixedDemandFunction()
env = Environment(simulation_length, demand_function)
q_agent = QAgent(env.action_space.n)
fixed_agent = FixedAgent()

env.add_agent(q_agent)
env.add_agent(fixed_agent)
reward_points = []
price_points = []

for x in trange(simulation_length):
    prices, rewards, _ = env.step()

    price_points.append(prices[0])
    reward_points.append(rewards[0])

plt.plot(list(range(simulation_length)), price_points, marker="o")
plt.plot(list(range(simulation_length)), reward_points, marker="o", color="blue")

plt.show()