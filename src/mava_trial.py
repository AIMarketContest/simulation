"""Example running discrete MADDPG on pettinzoo MPE environments."""


"""Example running MADQN on debug MPE environments."""
import functools
from datetime import datetime
from typing import Any

import launchpad as lp
import sonnet as snt
from absl import app, flags

from mava.components.tf.modules.exploration import LinearExplorationScheduler
from mava.systems.tf import madqn
from mava.utils import lp_utils
import pettingzoo_utils
from mava.utils.loggers import logger_utils

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "env_class",
    "mpe",
    "Pettingzoo environment class, e.g. atari (str).",
)

flags.DEFINE_string(
    "env_name",
    "simple_spread_v2",
    "Pettingzoo environment name, e.g. pong (str).",
)
flags.DEFINE_string(
    "mava_id",
    str(datetime.now()),
    "Experiment identifier that can be used to continue experiments.",
)
flags.DEFINE_string("base_dir", "~/mava", "Base dir to store experiments.")


def main(_: Any) -> None:

    # Environment.
    environment_factory = functools.partial(
        pettingzoo_utils.make_environment,
        env_class=FLAGS.env_class,
        env_name=FLAGS.env_name,
    )

    # Networks.
    network_factory = lp_utils.partial_kwargs(madqn.make_default_networks)

    # Checkpointer appends "Checkpoints" to checkpoint_dir
    checkpoint_dir = f"{FLAGS.base_dir}/{FLAGS.mava_id}"

    # Log every [log_every] seconds.
    log_every = 10
    logger_factory = functools.partial(
        logger_utils.make_logger,
        directory=FLAGS.base_dir,
        to_terminal=True,
        to_tensorboard=True,
        time_stamp=FLAGS.mava_id,
        time_delta=log_every,
    )

    # distributed program
    program = madqn.MADQN(
        environment_factory=environment_factory,
        network_factory=network_factory,
        logger_factory=logger_factory,
        num_executors=1,
        exploration_scheduler_fn=LinearExplorationScheduler(),
        importance_sampling_exponent=0.2,
        optimizer=snt.optimizers.Adam(learning_rate=1e-4),
        checkpoint_subpath=checkpoint_dir,
    ).build()

    # Ensure only trainer runs on gpu, while other processes run on cpu.
    local_resources = lp_utils.to_device(
        program_nodes=program.groups.keys(), nodes_on_gpu=["trainer"]
    )

    # Launch.
    lp.launch(
        program,
        lp.LaunchType.LOCAL_MULTI_PROCESSING,
        terminal="current_terminal",
        local_resources=local_resources,
    )


if __name__ == "__main__":
    app.run(main)


# import functools
# from datetime import datetime
# from typing import Any

# import launchpad as lp
# import sonnet as snt
# from absl import app, flags
# from mava.systems.tf import maddpg
# from mava.utils import lp_utils
# from mava.utils.loggers import logger_utils

# import pettingzoo_utils as pettingzoo_utils

# FLAGS = flags.FLAGS

# flags.DEFINE_string(
#     "env_class",
#     "mpe",
#     "Pettingzoo environment class, e.g. atari (str).",
# )

# flags.DEFINE_string(
#     "env_name",
#     "simple_speaker_listener_v3",
#     "Pettingzoo environment name, e.g. pong (str).",
# )
# flags.DEFINE_string(
#     "mava_id",
#     str(datetime.now()),
#     "Experiment identifier that can be used to continue experiments.",
# )
# flags.DEFINE_string("base_dir", "~/mava", "Base dir to store experiments.")


# def main(_: Any) -> None:
#     # Environment.
#     environment_factory = functools.partial(pettingzoo_utils.make_environment)

#     # Networks.
#     network_factory = lp_utils.partial_kwargs(maddpg.make_default_networks)

#     # Checkpointer appends "Checkpoints" to checkpoint_dir.
#     checkpoint_dir = f"{FLAGS.base_dir}/{FLAGS.mava_id}"

#     # Log every [log_every] seconds.
#     log_every = 10
#     logger_factory = functools.partial(
#         logger_utils.make_logger,
#         directory=FLAGS.base_dir,
#         to_terminal=True,
#         to_tensorboard=True,
#         time_stamp=FLAGS.mava_id,
#         time_delta=log_every,
#     )

#     # Distributed program.
#     program = maddpg.MADDPG(
#         environment_factory=environment_factory,
#         network_factory=network_factory,
#         logger_factory=logger_factory,
#         num_executors=1,
#         policy_optimizer=snt.optimizers.Adam(learning_rate=1e-2),
#         critic_optimizer=snt.optimizers.Adam(learning_rate=1e-2),
#         checkpoint_subpath=checkpoint_dir,
#         max_gradient_norm=1.0,
#     ).build()

#     # Ensure only trainer runs on gpu, while other processes run on cpu.
#     local_resources = lp_utils.to_device(
#         program_nodes=program.groups.keys(), nodes_on_gpu=["trainer"]
#     )

#     # Launch.
#     lp.launch(
#         program,
#         lp.LaunchType.LOCAL_MULTI_PROCESSING,
#         terminal="current_terminal",
#         local_resources=local_resources,
#     )


# if __name__ == "__main__":
#     app.run(main)
