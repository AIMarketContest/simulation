import pathlib
import typing
from string import Template

from ai_market_contest.cli.cli_config import (
    DEMAND_FUNCTION_DIR_NAME,
    DEMAND_FUNCTION_FILE,
)
from ai_market_contest.cli.utils.filesystemutils import check_overwrite


def create_demand_functon_class(
    demand_function_name: str, proj_dir: pathlib.Path, overwrite_check: bool = False
):
    demand_function_dir = proj_dir / DEMAND_FUNCTION_DIR_NAME
    demand_function_filename: str = f"{demand_function_name}.py"
    demand_function_file: pathlib.Path = demand_function_dir / demand_function_filename

    if (
        demand_function_file.exists()
        and overwrite_check
        and not check_overwrite(demand_function_filename, demand_function_dir)
    ):
        return

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
