# from ai_market_contest.training.policy_config_maker import PolicyConfigMaker
# from ai_market_contest.cli.utils.agent_locator import AgentLocator
# from ai_market_contest.training.policy_selector import PolicySelector
# from ai_market_contest.cli.addagentsubcommand import create_agent
# from ai_market_contest.cli.utils.project_initialisation_utils import make_main_config_file, make_agents_classes
#
# import pathlib
#
#
# def test_policy_config_maker(tmp_path: pathlib.Path):
#     make_proj_dir(tmp_path)
#     make_main_config_file(tmp_path, ["test_agent"], ["test"])
#     create_agent(tmp_path, "test_agent")
#
#     agent_locator = AgentLocator(tmp_path / "agents")
#     policy_selector = PolicySelector(agent_name="test_agent")
#     policy_config_maker = PolicyConfigMaker(agent_locator, policy_selector)
#
#     # TODO :: fix?
#     # policy_config_maker.get_policy_config()
#
#     # TODO :: assert some stuff
#
#
#
# def test_temp_path_stuff(tmp_path: pathlib.Path):
#     f = open(tmp_path / "file.txt", "a")
#     f.write("test")
#     f.close()
#
#     f = open(tmp_path / "file.txt", "r")
#     assert f.read() == "test"
