from ai_market_contest.cli.initsubcommand import make_main_config_file, make_proj_dir, make_environment_config_file, \
    remove_proj_dir, initialise_file_structure


def test_make_and_remove_proj_dir(tmp_path):
    make_proj_dir(tmp_path)
    assert (tmp_path / "agents").is_dir()
    assert (tmp_path / "environments").is_dir()
    assert (tmp_path / "environments" / "demandfunctions").is_dir()
    assert (tmp_path / "evaluation_configs").is_dir()
    assert (tmp_path / "training_configs").is_dir()

    remove_proj_dir(tmp_path)
    assert not (tmp_path / "agents").is_dir()
    assert not (tmp_path / "environments").is_dir()
    assert not (tmp_path / "environments" / "demandfunctions").is_dir()
    assert not (tmp_path / "evaluation_configs").is_dir()
    assert not (tmp_path / "training_configs").is_dir()


def test_make_main_config_file(tmp_path):
    make_proj_dir(tmp_path)
    make_main_config_file(tmp_path, ["test_agent"], ["test"])

    config_file = tmp_path / "config.ini"
    assert config_file.exists()

    assert (
        config_file.read_text()
        ==
        "[agent]\nagents = ['test_agent']\nauthors = ['test']\n\n"
    )


def test_make_environment_config_file(tmp_path):
    make_proj_dir(tmp_path)
    make_environment_config_file(tmp_path)

    config_file = tmp_path / "environments" / "config.ini"
    assert config_file.exists()

    assert (
        config_file.read_text()
        ==
        "[environment]\ndemandfunctions = []\n\n"
    )


def test_initialise_file_structure_does_all(tmp_path):
    initialise_file_structure(tmp_path, ["test_agent"], ["test"])

    assert (tmp_path / "agents").is_dir()
    assert (tmp_path / "environments").is_dir()
    assert (tmp_path / "environments" / "demandfunctions").is_dir()
    assert (tmp_path / "evaluation_configs").is_dir()
    assert (tmp_path / "training_configs").is_dir()

    env_config_file = tmp_path / "environments" / "config.ini"
    assert env_config_file.exists()

    assert (
            env_config_file.read_text()
            ==
            "[environment]\ndemandfunctions = []\n\n"
    )

    config_file = tmp_path / "config.ini"
    assert config_file.exists()

    assert (
        config_file.read_text()
        ==
        "[agent]\nagents = ['test_agent']\nauthors = ['test']\n\n"
    )

