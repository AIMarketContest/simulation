# Getting Started Tutorial

Here we give a top-level introduction on how to get started with the AI Contests toolbox.

Firstly ensure that you have correctly installed the project as described in the README.


## Creating the project directory

First we must have a directory to hold the structure of the toolbox. This can be created simply with the following command:

`aic init`

You will then be prompted to enter an author name. The next step is to create an initial agent, select custom from the options and then call it AgentX. You should see the following:

```
Enter name(s) of the author(s): Jane Doe 
? What type of agent would you like to start with (you can add more after initialising the project)? custom
Enter custom agent name: AgentX
```

Your project structure should now be:
```
aicontest/
├── agents
│   └── AgentX
│       ├── AgentX.py
│       ├── config.ini
│       └── trained-agents
│           └── 00a11e938af2edefacceffe60ea22fbb1e9e34b7
│               └── metadata.ini
├── config.ini
├── environments
│   ├── config.ini
│   └── demandfunctions
├── evaluation_configs
│   └── evaluation_example_config.ini
└── training_configs
    └── training_example_config.ini
```

**Note:** The hash in `trained-agents` will be different.

The `agents` folder will be where all custom agents are coded and their trained derivatives will be stored.

The `environments` folder will allow you to store any custom demand functions. These can be found in the `demandfunctions` folder inside.

We have the directories for `training_configs` and `evaluation_configs`. These directories hold the configuration files in use.

## Agents

### Main agent file

Now let's have a look at (a trimmed down version of) the file `AgentX.py`:

```python
class AgentX(Agent):

    def __init__(self, observation_space=None, action_space=None, config={}):
        super().__init__(observation_space, action_space, config)

    def get_initial_price(self) -> Price:
        raise NotImplementedError

    def policy(
        self, last_round_all_agents_prices: list[Price], identity_index: int
    ) -> Price:
        raise NotImplementedError

    def update(self, last_round_profit: Price, identity_index: int) -> None:
        pass
```

As you can see there are three main functions.

The method `get_initial_price` finds the agents' first price.

The method `policy` is called to query the agent for it's new price.

Finally, the method `update` is called to tell the agent more information about the rounds so that it can alter it's strategy accordingly. This will be called between every timestep with the profit earned last timestep.

We now implement `AgentX` to be a simple q-agent so we can watch it train.

```python
from collections import defaultdict
from functools import partial
from typing import Sequence

import numpy as np

from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price


class AgentX(Agent):
    def __init__(self, observation_space=None, action_space=None, config={}):
        super().__init__(observation_space, action_space, config)
        self.cost = 0.3
        self.actions_spaces = 100
        self.Q: dict[Sequence[float], dict[float, float]] = defaultdict(
            partial(defaultdict, int)
        )
        self.alpha = 0.3
        self.gamma = 0.9
        self.theta = 0.0005
        self.time = 0
        self.last_round_prices: list[Price] = []
        self.last_round_profit = 0

    def get_initial_price(self) -> Price:
        return 1

    def policy(
        self, last_round_all_agents_prices: list[Price], identity_index: int
    ) -> Price:
        self.last_round_prices = last_round_all_agents_prices
        other_agent_prices = (
            last_round_all_agents_prices[:identity_index]
            + last_round_all_agents_prices[identity_index + 1 :]
        )

        if (
            tuple(other_agent_prices) in self.Q
            and np.random.uniform(0, 1) > self.probability_exploration()
        ):
            previous_actions_for_state = self.Q[tuple(other_agent_prices)]

            max_profit: float = 0.0
            best_price: float = 0.0
            for price, profit in previous_actions_for_state.items():
                if profit > max_profit:
                    max_profit = profit
                    best_price = price

            return int(best_price)

        return np.random.randint(0, self.actions_spaces)

    def update(
        self,
        last_round_profit: int,
        identity_index: int,
    ) -> None:
        if not self.last_round_prices:
            return

        a1 = self.last_round_prices[identity_index]

        other_agent_prices = (
            self.last_round_prices[:identity_index]
            + self.last_round_prices[identity_index + 1 :]
        )

        max_path: float = np.argmax(self.Q[tuple(other_agent_prices)])  # type: ignore
        self.Q[tuple(other_agent_prices)][a1] += self.alpha * (
            last_round_profit
            + self.gamma * max_path
            - self.Q[tuple(other_agent_prices)][a1]
        )

    def probability_exploration(self):
        return (1 - self.theta) ** self.time

    def learning_has_converged(self):
        return True
```

We now have a basic agent.

## Training

### Configuring the training session

If we look in `training_configs` we already see a training configuration file called called `training_example_config.ini` there. Let's take a look at it:

```ini
[General]
number_of_self_play_agents = 2
demand_function = Fixed
simulation_length = 200
optimisation_algorithm = DQN
epochs = 20
print_training = False

[Naive Agents]
FixedFifty = 3
Random = 1

[Other] # To get passed as an RLlib config
num_workers = 4
```

As we can see here the file contains three main sections.

The section `General` contains important information about the simulation that will train our agents. We see the number of self play agents (how many copies of the agent you are trying to train should be included in the simulation), the demand function to use and more.
Please see the documentation on configurations to learn more about the options available.
For now, let's change the demand function from `Fixed` to `Gaussian`. The project comes with a few predefined demand functions for you already and later we will also demonstrate how to define your own.

The section `Naive Agents` defines which pre-defined non-learning agents should be included in the simulations and their counts. In this file we are including 3 FixedFifty agents and 1 Random agent.
For more detail on the given agents please see the documentation on configuration files.

The `other` section helps interface with RLlib directly and configure their training routines. This helps give you better control over more complex training routines. Changing this section is outside the scope of this tutorial.

### Running the training session

Now that we have a new configuration file defined (changing the demand function from `Fixed` to `Gaussian`) we can train our new agent.

We run: 
```
aic train
```
Then choose an agent to train (`AgentX`), the version of agent to train (the first and only one) and the training configuration to run the training (`example_training_config`). We can fill in the training message to keep track of why we trained the agent as we did at each step, we will write "Initial training with Gaussian demand function, 2 FixedFifty agents and a Random agents". Do not worry about writing all the details down, the program will store the exact configuration along with your agent!

With that our agent should be training. Once we have finished we look at the project tree directory and see

```
aicontest/
├── agents
│   └── AgentX
│       ├── AgentX.py
│       ├── config.ini
│       └── trained-agents
│           ├── 00a11e938af2edefacceffe60ea22fbb1e9e34b7
│           │   └── metadata.ini
│           └── 9321a549940764b1abd394600619b7d87a0365dd
│               ├── metadata.ini
│               ├── trained_config.ini
│               └── trained.pkl
├── config.ini
├── environments
│   ├── config.ini
│   └── demandfunctions
├── evaluation_configs
│   └── evaluation_example_config.ini
└── training_configs
    └── training_example_config.ini
```

Notice that AgentX now has a second hash in `trained-agents` containing some checkpoints, a configuration file and some metadata. If we look at the metadata we see information about the training, including when the agent was trained, the message written and which version it is a derivative of. If we look at the configuration file we see the exact configuration used to train the agent.
Feel free to explore the files.

### Training a new generation

Now suppose we wanted to further improve the training of our agent by letting it train with a custom demand function.
Let's design a lowest takes all demand function where the agent with the lowest price receives all the sales.

First we run
``` 
aic add-demand-function
```

When prompted we add the name `LowestGreedy`.

Now open up the file and implement as follows:
```python
from ai_market_contest.demand_function import DemandFunction


class LowestGreedy(DemandFunction):
    MAX_SALES_SCALE_FACTOR: int = 1000

    def __init__(self):
        pass

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        sales: dict[str, int] = {agent: 0 for agent in current_prices.keys()}
        min_agents = []
        min_price = float("inf")

        for agent, price in current_prices.items():
            if price == min_price:
                min_agents.append(agent)
            elif price < min_price:
                min_agents = [agent]
                min_price = price

        agent_sales = int(self.MAX_SALES_SCALE_FACTOR / len(min_agents))
        for agent in min_agents:
            sales[agent] = agent_sales

        return sales
```

We now write a configuration file to use the new demand function.

We can run the following command to make a new training configuration.

```
aic add-train-config
```

Enter the name `greedy_training_config`.

Open up the file and set the demand function to `LowestGreedy`.

We now run
```
aic train
```

Select AgentX. You will now see two different options for the version, select the latest version to continue the training. Select the config we just defined, namely `greedy_training_config`.
Give the training a useful message such as `Trained against lowest greedy demand function`.

### Training RLlib agents

We can train pre-made RLlib agents.

First we need to define a new agent in our project.

Run
```
aic add-agent
```

When prompted select, RLlib agent and choose one from the list.
Call the agent `RLlibTest`

When training RLlib agents, we need to specify this in our configuration.
Let's start a new configuration.

```
aic add-train-config
```

Call the configuration file, `rllib_triple_self_play`.

Now let us edit the configuration.

You **cannot** train RLlib agents with other agents, only via self play, so delete the `Naive Agents` section.
Now as the name of the file suggests, let's change the number of self play agents to 3.

We then go through the the training settings again.
```
aic train
```
Select `RLlibTest` from the list of agents.
You will notice now there is only one version as it is a new agent, select it.
Select the training configuration we just defined and add the training message `Train against 3 versions`.

### Training agents with other trained agents
Now say, you wanted to measure the impact of training our `AgentX` with `RLlibTest`.
As usual, as it is a configuration we have not used yet we need to write a new file.

```
aic add-train-config
```

Call the configuration `train_against_rllib_test`.

Let's keep the naive agents in the simulation as well, we just want to add `RLlibTest`.

Copy this section, converting to your program as necessary, into your configuration file:

```
[Trained Agents]
RLlibTest = ('55b8f4fkkkk4833856df2f435c0c2073d9eece2d5ab2', 3)
```

**Be sure to change the hash to your trained agent hash in single quotes**

We see that the key is name of the agent to load, the first element of the set is the hash of the trained agent to load, and the second number is the count.

We then start up the usual
```
aic train
```
Select `AgentX` and the latest version. Select `train_against_rllib_test` from the configuration. Give a training message such as `Train against RLlibTest`.

### Training a previous version
If we wanted to find out the effects of training against `RLlibTest` before we trained against our `LowestGreedy` demand function we can set this up simply.
Run
```
aic train
```
Select `AgentX` from the list and, instead of picking the latest version, pick the version `Initial training with Gaussian demand function, 2 FixedFifty agents and a Random agents"`.
We can then pick the training configuration we made beforehand, `train_against_rllib_test`.
Add the training message `Train against RLlibTest after Gaussian demand function training`.
It is worth noting the program will keep track of the history and parents of each version for you so there is no need to worry about forgetting the order.


## Contest
Now let's see how the `GreedyLowest AgentX`, `RLlibTest` trained `AgentX` and `RLlibTest` compete against each other.

First we want to write a custom configuration file so we write:
```
aic add-evaluate-config
```

Name the config `gaussian_450_length`.
Change the simulation length to 450 in the configuration file we just made.

Now we write
```
aic evaluate
```

Select `AgentX`, then select the version trained with `GreedyLowest`.
Select `AgentX` again, then select the version trained against `RLlibTest`.
Select `RlLibTest` and select the latest version.
Select `exit`.

Load in the configuration `gaussian_450_length` by selecting it from the list.

Now we can see the results!

It is worth noting that you might want to run contests between training to ensure that your agents are only improving. If they are not you can just continue training from the parent.
