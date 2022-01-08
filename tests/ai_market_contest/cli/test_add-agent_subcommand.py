# """
# # Behaviour:
# - Adds agent to the given path
# """
#
# import io
# import sys
#
# from cli_test_utils import check_is_agent, initialise_main_folder, run_cli_command
#
#
# def test_adds_agent_to_given_path(parser, tmp_path):
#     agent_name = "AgentName"
#     author_name = "Author Name"
#     initialise_main_folder(
#         parser, tmp_path, agent_name=agent_name, author_name=author_name
#     )
#
#     extra_agent_name = "ExtraAgent"
#     assert extra_agent_name != agent_name
#
#     # input for the program once it runs
#     sys.stdin = io.StringIO(f"{extra_agent_name}\n{author_name}\n")
#     run_cli_command(parser, ["add-agent", str(tmp_path)])
#     check_is_agent(tmp_path, extra_agent_name)
