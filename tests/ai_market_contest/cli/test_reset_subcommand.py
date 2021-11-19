"""
# Behaviour:
 - deletes project folder
 - exits with non-zero exit code when trying to remove a project
   that has not been created
"""
import os

import pytest
from cli_test_utils import initialise_main_folder, run_cli_command


def test_reset_removes_project_folder(tmp_path, parser):
    initialise_main_folder(parser, tmp_path)
    run_cli_command(parser, ["reset", str(tmp_path)])
    assert not os.path.isdir(tmp_path / "aicontest"), "Project folder not removed"


def test_non_zero_exit_code_when_resetting_project_not_created(tmp_path, parser):
    with pytest.raises(SystemExit) as e:
        run_cli_command(parser, ["reset", str(tmp_path)])
    assert e.type == SystemExit
    assert e.value.code != 0
