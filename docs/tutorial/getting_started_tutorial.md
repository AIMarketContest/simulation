Here we give a top-level introduction on how to get started with the AI Contests toolbox.

Firstly ensure that you have correctly set up the dependencies as described in the README.



# Creating the project directory

First we must have a directory to hold the structure of the toolbox. This can be created simply with the following command:

`aic init .`

You will then be prompted to enter a name for an initial agent and author. Fill them in as follows:

```
Enter name of agent 1: AgentX
Enter name(s) of the author(s): Jane Doe
```

Your project structure should now be:

```
aicontest/
├── agents
│   └── AgentX
│       ├── AgentX.py
│       ├── config.ini
│       ├── initial_pickler.py
│       └── trained-agents
│           └── c4cc5ef3a97ebc149e47c32f3d095f2d85995e2f
│               └── metadata.ini
├── config.ini
├── environments
└── training_configs
```

**Note:** The hash in `trained-agents` will be different.

The `agents` folder will be where all custom agents are coded and their trained derivatives will be stored.

The `environments` folder will allow you to store any custom demand functions.



# Agents

## Main agent file

Now let's have a look at (a trimmed down version of) the file `AgentX.py`:

```python
from ai_market_contest.agent import Agent
class AgentX(Agent):

    def policy(
        self, last_round_agents_prices: list[float], identity_index: int
    ) -> float:
        raise NotImplementedError

    def learning_has_converged(self):
        raise NotImplementedError

    def update(
        self,
        last_round_prices: list[float],
        last_round_sales: int,
        round_before_last_prices: list[float],
        round_before_last_sales: int,
        identity_index: int,
    ) -> None:
        raise NotImplementedError
```

As you can see there are three main functions.

The method `policy` is called to query the agent for it's new price.

The method `update` is called to tell the agent more information about the rounds so that it can alter it's strategy accordingly.

Finally, the method `learning_has_converged` should give an indication of whether the agent has reached a stable strategy.



We will now implement the class to resemble a non-learning naïve implementation, namely an agent that returns a random number at every query. Fill in the functions as follows:

```python
import random

from ai_market_contest.agent import Agent


class AgentX(Agent):
    """
    An agent which returns a random price.
    """

    def update(
        self,
        last_round_prices: list[float],
        last_round_sales: int,
        round_before_last_prices: list[float],
        round_before_last_sales: int,
        identity_index: int,
    ) -> None:
        pass

    def policy(self, last_round_agents_prices: list[float], agent_index: int) -> float:
        return random.random()

    def learning_has_converged(self):
        return True

```

We now have a basic agent.

## Pickler

The project also requires you to implement a basic file that can instantiate your agent. A template can be found in `initial_pickler.py` and should be edited to be specific to your new agent. In this case the program has correctly written the file for you and we shall see a specific example of when a more complicated instantiation should take place.

```python
import pathlib
import pickle

from AgentX import AgentX

INITIAL_PICKLE_FILE_NAME = "initial_pickle.pkl"

agent = AgentX()

pickle_file = (pathlib.Path(__file__).parent) / INITIAL_PICKLE_FILE_NAME

with pickle_file.open("wb") as pkl:
    pickle.dump(agent, pkl)

```

## Initialisation

Now that a *pickler* has been defined we can initialise our new agent. We must type in the following command where `{path}` is the path to the directory that holds the `aicontest` project folder.

```
aic initialise-agent {path}
```

We will then be met with a selection of agents and we pick the new agent we created we wish to initialise:

```
The current initialised agents are:
[AgentX]
Choose an agent to initialise: AgentX
Agent successfully initialised
```

If we look at the `trained-agents` directory we can see that it now contains a pkl file. 

The agent is now ready to train.

# Training

## Configuring the training session

Create a new document in `aicontest/training_configs` called `our_naive_train_config.py`.

Fill it in as follows:

```python
from ai_market_contest.cli.training_config.naive_agent_training_config import NaiveAgentTrainingConfig
from ai_market_contest.agents.fixed_agent import FixedAgent
from ai_market_contest.agents.random_agent import RandomAgent
from ai_market_contest.demandfunctions.gaussian_demand_function import GaussianDemandFunction

def get_config():
    config = NaiveAgentTrainingConfig()

    config.add_naive_agent(FixedAgent(12))
    config.add_naive_agent(FixedAgent(88))
    config.add_naive_agent(RandomAgent())
    config.add_naive_agent(RandomAgent())
    config.add_naive_agent(RandomAgent())
    config.add_naive_agent(RandomAgent())
    config.add_naive_agent(RandomAgent())
    config.add_naive_agent(RandomAgent())

    config.set_demand_function(GaussianDemandFunction())

    config.set_training_duration(1500)

    return config

```

The most important aspect of this file is that it defines a `get_config()`method that returns a valid config.

In this training session we chose to go with a naive agent training session, there is also a self play training session.

## Running the training session

Now that we have a valid training configuration, we can run the training session. Replacing path to the folder that holds the `aicontest` folder, type in the command:

 `aic train {path}`

Then choose an agent to train (`AgentX`), the generation of agent to train (`0`) and the training configuration to run the training (`our_naive_train_config`). We can fill in the training message to keep track of why we trained the agent as we did at each step, we will write "Initial training with naive fixed price and random priced bots". Do not worry about writing all the details down, the program will store the exact configuration along with your agent!

```
The current agents are:
[AgentX]
Choose an agent to train: AgentX

0 c4cc5e 2021-11-24 12:28:00.619215 Initial untrained agent

Input the hash or index of the version of the agent to be trained: 0
The current training configs are:
[our_naive_train_config]
Choose a training config: our_naive_train_config
(Optional) Enter training message: Initial training with naive fixed price and random priced bots
```

If we look at the project tree directory we see:

```
aicontest/
├── agents
│   └── AgentX
│       ├── AgentX.py
│       ├── __pycache__
│       │   └── AgentX.cpython-39.pyc
│       ├── config.ini
│       ├── initial_pickler.py
│       └── trained-agents
│           ├── 3fab47c53198e2cb4d1a17c406cfb9f411767f03
│           │   ├── agent_pickle.pkl
│           │   ├── metadata.ini
│           │   └── train_config.ini
│           └── c4cc5ef3a97ebc149e47c32f3d095f2d85995e2f
│               ├── agent_pickle.pkl
│               └── metadata.ini
├── config.ini
├── environments
└── training_configs
    ├── __pycache__
    │   └── our_naive_train_config.cpython-39.pyc
    └── our_naive_train_config.py
```

Notice that AgentX now has a second hash in `trained-agents` containing the trained agent's pkl file, metadata about the training (such as the time and generation it has been trained from) and the configuration used to train that generation. Feel free to explore those files.

## Training a new generation

Now suppose we wanted to further improve the training of our agent with some self play training.

We make a new training configuration file in `training_configs` called `our_self_play_train_config.py` and fill it in as follows:

```python
from ai_market_contest.cli.training_config.self_play_training_config import SelfPlayTrainingConfig
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction

def get_config():
    config = SelfPlayTrainingConfig()

    config.set_number_of_agents(12)

    config.set_demand_function(FixedDemandFunction(15))

    config.set_training_duration(1350)

    return config
```

As you can see, there is no longer the ability to add naïve agents implementations and that is replaced with the option of how many copies of the agent you want in the game.

As before you run:

```
aic train {path}
```

Choose AgentX, and now you see that there is a new generation of trained agent. We pick the newest generation by typing in 1, corresponding to the agent with the most recent time stamp:

```
The current agents are:
[AgentX]
Choose an agent to train: AgentX

0 c4cc5e 2021-11-24 12:28:00.619215 Initial untrained agent

1 3fab47 2021-11-24 12:46:31.257774 Initial training with naive fixed price and random priced bots

Input the hash or index of the version of the agent to be trained: 1
```

Now in the list of configuration files we see the our latest file and we select it by typing it in. We also add a message "Self play with 12 other copies":

```
The current training configs are:
[our_self_play_train_config, our_naive_train_config]
Choose a training config: our_self_play_train_config
(Optional) Enter training message: Self play with 12 other copies
```

One final check to the directory structure shows it worked in a similar way to before:

```
aicontest/
├── agents
│   └── AgentX
│       ├── AgentX.py
│       ├── __pycache__
│       │   └── AgentX.cpython-39.pyc
│       ├── config.ini
│       ├── initial_pickler.py
│       └── trained-agents
│           ├── 3fab47c53198e2cb4d1a17c406cfb9f411767f03
│           │   ├── agent_pickle.pkl
│           │   ├── metadata.ini
│           │   └── train_config.ini
│           ├── a4c553ef75d3d1382c22ee02668455f529069e8c
│           │   ├── agent_pickle.pkl
│           │   ├── metadata.ini
│           │   └── train_config.ini
│           └── c4cc5ef3a97ebc149e47c32f3d095f2d85995e2f
│               ├── agent_pickle.pkl
│               └── metadata.ini
├── config.ini
├── environments
└── training_configs
    ├── __pycache__
    │   ├── our_naive_train_config.cpython-39.pyc
    │   └── our_self_play_train_config.cpython-39.pyc
    ├── our_naive_train_config.py
    └── our_self_play_train_config.py
```

# Adding a new agent

Now that we have trained our first agent, we want to add in a new agent to train.

We run the following command:

```
aic add-agent {path}
```

We then enter the name for our new agent:

```
Enter name of new agent: AgentY
```

We should now have a project structure as follows:

```
aicontest/
├── agents
│   └── AgentX
│       ├── AgentX.py
│       ├── __pycache__
│       │   └── AgentX.cpython-39.pyc
│       ├── config.ini
│       ├── initial_pickler.py
│       └── trained-agents
│           ├── 3fab47c53198e2cb4d1a17c406cfb9f411767f03
│           │   ├── agent_pickle.pkl
│           │   ├── metadata.ini
│           │   └── train_config.ini
│           ├── a4c553ef75d3d1382c22ee02668455f529069e8c
│           │   ├── agent_pickle.pkl
│           │   ├── metadata.ini
│           │   └── train_config.ini
│           └── c4cc5ef3a97ebc149e47c32f3d095f2d85995e2f
│               ├── agent_pickle.pkl
│               └── metadata.ini
├── config.ini
├── environments
└── training_configs
    ├── __pycache__
    │   ├── our_naive_train_config.cpython-39.pyc
    │   └── our_self_play_train_config.cpython-39.pyc
    ├── our_naive_train_config.py
    └── our_self_play_train_config.py
```

We implement the agent interface by filling in the `AgentY.py` file as follows:

```python
from ai_market_contest.agent import Agent


class AgentY(Agent):

    def __init__(self, price: int):
        self.price = price

    def update(
        self,
        last_round_prices: list[float],
        last_round_sales: int,
        round_before_last_prices: list[float],
        round_before_last_sales: int,
        identity_index: int,
    ) -> None:
        pass

    def learning_has_converged(self):
        return True

    def policy(self, last_round_agents_prices: list[float], agent_index: int) -> float:
        return self.price
```

This agent returns the same price every time it is requested.

What is interesting about this agent is that it has a more complicated instantiation procedure and so requires modifications to the  `AgentY/initial_pickler.py`file. Change it as follows:

```python
import pathlib
import pickle

from AgentY import AgentY

INITIAL_PICKLE_FILE_NAME = "initial_pickle.pkl"

agent = AgentY(70) # This is the line we have changed

pickle_file = (pathlib.Path(__file__).parent) / INITIAL_PICKLE_FILE_NAME

with pickle_file.open("wb") as pkl:
    pickle.dump(agent, pkl)
```

Notice that we now supply all arguments that `AgentY` requires.

We now initialise the agent with the command:

```
aic initialise-agent {path}
```

And when prompted with the following we select the correct agent:

```
The current uninitialised agents are:
[AgentX, AgentY]
Choose an agent to initialise: AgentY
Agent successfully initialised
```

We then proceed to train AgentY in the same way as above:

```
aic train {path}
```

We notice that now there is only 1 generation of agent, the one we have just initialised, and we select it. We also select our naive training configuration with message "Initial training with naive fixed price and random priced bots":

```
The current agents are:
[AgentX, AgentY]
Choose an agent to train: AgentY

0 d80b96 2021-11-24 12:59:35.041439 Initial untrained agent

Input the hash or index of the version of the agent to be trained: 0
The current training configs are:
[our_self_play_train_config, our_naive_train_config]
Choose a training config: our_naive_train_config
(Optional) Enter training message: Initial training with naive fixed price and random priced bots
```

We take a final look at our folder structure:

```
aicontest/
├── agents
│   ├── AgentX
│   │   ├── AgentX.py
│   │   ├── __pycache__
│   │   │   └── AgentX.cpython-39.pyc
│   │   ├── config.ini
│   │   ├── initial_pickler.py
│   │   └── trained-agents
│   │       ├── 3fab47c53198e2cb4d1a17c406cfb9f411767f03
│   │       │   ├── agent_pickle.pkl
│   │       │   ├── metadata.ini
│   │       │   └── train_config.ini
│   │       ├── a4c553ef75d3d1382c22ee02668455f529069e8c
│   │       │   ├── agent_pickle.pkl
│   │       │   ├── metadata.ini
│   │       │   └── train_config.ini
│   │       └── c4cc5ef3a97ebc149e47c32f3d095f2d85995e2f
│   │           ├── agent_pickle.pkl
│   │           └── metadata.ini
│   └── AgentY
│       ├── AgentY.py
│       ├── __pycache__
│       │   └── AgentY.cpython-39.pyc
│       ├── config.ini
│       ├── initial_pickler.py
│       └── trained-agents
│           ├── 779cd8f8df32bb9e30681bd44630edcc14b01193
│           │   ├── agent_pickle.pkl
│           │   ├── metadata.ini
│           │   └── train_config.ini
│           └── d80b960711a12b61ec282ffdceacef1a4da36434
│               ├── agent_pickle.pkl
│               └── metadata.ini
├── config.ini
├── environments
└── training_configs
    ├── __pycache__
    │   ├── our_naive_train_config.cpython-39.pyc
    │   └── our_self_play_train_config.cpython-39.pyc
    ├── our_naive_train_config.py
    └── our_self_play_train_config.py
```

