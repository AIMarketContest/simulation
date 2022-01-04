import pathlib
import typing
from string import Template

from cli_config import DEMAND_FUNCTION_DIR_NAME, DEMAND_FUNCTION_FILE


def create_demand_functon_class(
    demand_function_name: str, proj_dir: pathlib.Path, check_overwrite: bool = False
):
    demand_function_dir = proj_dir / DEMAND_FUNCTION_DIR_NAME
    demand_function_filename: str = f"{demand_function_name}.py"
    demand_function_file: pathlib.Path = demand_function_dir / demand_function_filename
    # TODO: Add overwriting functionality again
    # if check_overwrite:
    #     check_overwrite_agent(agent_filename, agent_dir)
    demand_function_file.touch()
    create_new_demand_function_file(demand_function_file, demand_function_name)


def create_new_demand_function_file(
    demand_function_file: pathlib.Path, demand_function_name: str
):
    subs: typing.Dict[str, str] = {"demand_function_classname": demand_function_name}
    with DEMAND_FUNCTION_FILE.open("r") as a_file:
        src = Template(a_file.read())
    with demand_function_file.open("w") as new_demand_function_file:
        new_demand_function_file.write(src.substitute(subs))
