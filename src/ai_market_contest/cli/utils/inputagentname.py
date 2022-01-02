def remove_underscores(string: str):
    return string.replace("_", "")


def is_valid_agent_name(agent_name: str):
    return agent_name[0].isalpha() and remove_underscores(agent_name).isalnum()


# def input_agent_name(agents_names: List[str]):
#     while True:
#         agent_name: str = input()
#         if is_valid_agent_name(agent_name):
#             if agent_name in agents_names:
#                 print("Two agents cannot have the same name")
#                 print("Please enter a valid agent name: ", end="")
#                 continue
#             break
#         print(
#             "Agent name must begin with a letter and can only contain letters, ",
#             "numbers and underscores",
#         )
#         print("Enter a valid agent name: ", end="")
#     return agent_name
