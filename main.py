import random
import gym
from gym import spaces
import numpy as np
import custom_env

# pip install:
# gym==0.25.2
# numpy
# tensorflow
# keras-rl2

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers.legacy import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

# creating own environment: https://www.gymlibrary.dev/content/environment_creation/
# using custom environment: https://stackoverflow.com/questions/45068568/how-to-create-a-new-gym-environment-in-openai
# initial tutorial: https://www.youtube.com/watch?v=YLa_KkehvGw&ab_channel=NeuralNine

gym.register(
    id="GridWorldEnv-v0",
    entry_point="custom_env:GridWorldEnv",
)

env = gym.make("GridWorldEnv-v0")  # CartPole-v1")

states = env.observation_space.spaces["agent"].shape[
    0
]  # env.observation_space.shape[0]
actions = env.action_space.n  # env.action_space.n

print(states)
print(actions)

model = Sequential()
model.add(Flatten(input_shape=(1, states)))
model.add(Dense(24, activation="relu"))
model.add(Dense(24, activation="relu"))
model.add(Dense(actions, activation="linear"))

agent = DQNAgent(
    model=model,
    memory=SequentialMemory(limit=50000, window_length=1),
    policy=BoltzmannQPolicy(),
    nb_actions=actions,
    nb_steps_warmup=10,
    target_model_update=0.01,
)

agent.compile(Adam(lr=0.001), metrics=["mae"])
agent.fit(env, nb_steps=100000, visualize=True, verbose=1)

results = agent.test(env, nb_episodes=10, visualize=True)
print(np.mean(results.history["episode_reward"]))

env.close()
