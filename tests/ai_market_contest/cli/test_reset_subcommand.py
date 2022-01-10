from importlib_metadata import pathlib

from ai_market_contest.cli.utils.project_initialisation_utils import initialise_file_structure
from ai_market_contest.cli.resetsubcommand import remove_proj_dir

def test_remove_proj_dir(tmp_path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["TestAgent"], ["Test"])

    assert tmp_path.exists()

    remove_proj_dir(tmp_path)

    assert not tmp_path.exists()

