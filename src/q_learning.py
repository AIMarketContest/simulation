import gym
import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import sys
from src.agent import Agent

from collections import defaultdict
import src.plotting as plotting
import src.environment as environment
import src.demandfunctions.fixed_demand_function as fixed_demand

"""
https://www.geeksforgeeks.org/q-learning-in-python/
Used this tutorial to understand rl algorithms in python and integration with pettingzoo
"""

matplotlib.style.use('ggplot')
simulation_length = 100
demand_function = fixed_demand.FixedDemandFunction()
env = environment.Environment(simulation_length, demand_function)


def createEpsilonGreedyPolicy(Q, epsilon, num_actions):
    """
    Creates an epsilon-greedy policy based
    on a given Q-function and epsilon.

    Returns a function that takes the state
    as an input and returns the probabilities
    for each action in the form of a numpy array
    of length of the action space(set of possible actions).
    """

    def policyFunction(state):
        Action_probabilities = np.ones(num_actions,
                                       dtype=float) * epsilon / num_actions
        # print(Q)
        # print(Q[state])
        best_action = np.argmax(Q[state[0]])
        Action_probabilities[best_action] += (1.0 - epsilon)
        return Action_probabilities

    return policyFunction


class QAgent(Agent):
    def __init__(self, env):
        self.curr_price = 0
        self.env = env
        self.cost = 0.3
        self.env.add_agent(self)

    def policy(self) -> float:
        return self.curr_price

    def get_reward(self, demand):
        return (self.curr_price - self.cost)*demand

    def qLearning(self, num_episodes, discount_factor=1.0,
                  alpha=0.6, epsilon=0.1):
        """
        Q-Learning algorithm: Off-policy TD control.
        Finds the optimal greedy policy while improving
        following an epsilon-greedy policy"""

        # Action value function
        # A nested dictionary that maps
        # state -> (action -> action-value).
        Q = defaultdict(lambda: np.zeros(self.env.action_space.n))
        print(Q[0])

        # Keeps track of useful statistics
        stats = plotting.EpisodeStats(
            episode_lengths=np.zeros(num_episodes),
            episode_rewards=np.zeros(num_episodes))

        # Create an epsilon greedy policy function
        # appropriately for environment action space
        policy = createEpsilonGreedyPolicy(Q, epsilon, self.env.action_space.n)

        # For every episode
        for ith_episode in range(num_episodes):

            # Reset the environment and pick the first action
            state = self.env.reset()
            # print("first state: " + str(state))
            for t in itertools.count():

                # get probabilities of all actions from current state
                action_probabilities = policy(state)

                # choose action according to
                # the probability distribution
                action = np.random.choice(np.arange(
                    len(action_probabilities)),
                    p=action_probabilities)

                # take action and get reward, transit to next state
                next_state, reward, done = self.env.step(action)
                if len(reward) == 0:
                    reward.append(0)
                    next_state.append(0)
                print(next_state)
                # Update statistics
                stats.episode_rewards[ith_episode] += self.get_reward(reward[0])
                stats.episode_lengths[ith_episode] = t

                # TD Update
                best_next_action = np.argmax(Q[next_state[0]])
                td_target = reward + discount_factor * Q[next_state[0]][best_next_action]
                td_delta = td_target - Q[state[0]][action]
                Q[state[0]][action] += alpha * td_delta

                # done is True if episode terminated
                if done:
                    break

                state[0] = next_state[0]
                self.curr_price = state/1000

        return Q, stats

    def update(
        self,
        last_round_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int
    ) -> None:
        return

q_agent = QAgent(env)
Q, stats = q_agent.qLearning(1000)
print(stats.episode_lengths.shape)
plotting.plot_episode_stats(stats)
