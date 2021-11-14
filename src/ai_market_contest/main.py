# observations = parallel_env.reset()
# max_cycles = 500
# for step in range(max_cycles):
#     actions = {
#         agent: agent.policy(observations[agent]) for agent in parallel_env.agents
#     }
#     observations, rewards, dones, infos = parallel_env.step(actions)


# if self.time_step > 1:
#     for agent_index, agent in enumerate(self.possible_agents):
#         agent.update(
#             self.hist_set_prices[-2],
#             self.hist_sales_made[-2][agent_index],
#             previous_prices,
#             self.hist_sales_made[-1][agent_index],
#             agent_index,
#         )
