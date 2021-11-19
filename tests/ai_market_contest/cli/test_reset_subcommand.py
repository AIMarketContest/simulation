import os

from cli_test_utils import (
    initialise_main_folder,
    run_cli_command,
)


def test_reset_removes_project_folder(tmp_path, parser):
    initialise_main_folder(parser, tmp_path)
    run_cli_command(parser, ["reset", str(tmp_path)])
    assert not os.path.isdir(tmp_path / "aicontest")
