from agents.q_learning import QAgent
from demandfunctions.gaussian_demand_function import GaussianDemandFunction
from environment import Environment
import matplotlib as plt

from utils.plotting import plot_episode_stats

plt.style.use("ggplot")
simulation_length = 100
demand_function = GaussianDemandFunction()
env = Environment(simulation_length, demand_function)
q_agent = QAgent(env)
Q, stats = q_agent.qLearning(1000)
plot_episode_stats(stats)
