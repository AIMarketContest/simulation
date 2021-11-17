"""
# Behaviour:
- Should create an aicontest folder at the given location
- Should take a -n flag specifying the number of agents to create at launch
- The -n flag should default to 1 agent
- The --include-example argument should include an example of running the
  program
"""

from unittest import TestCase

from cli import initialise_parser


class InitSubcommandTest(TestCase):
    parser = initialise_parser()

    def create_aicontest_folder_at_given_path(self):
        raise NotImplementedError

    def specify_number_of_agents_to_initialise_with_using_n_flag(self):
        raise NotImplementedError

    def default_number_of_agents_to_create_is_one(self):
        raise NotImplementedError

    def copy_example_usage_with_include_example_tag(self):
        raise NotImplementedError
