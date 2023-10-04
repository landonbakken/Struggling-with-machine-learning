# purely cosmetic things
import warnings
import os

warnings.warn = lambda *args, **kwargs: None
os.system("cls")

# start actual things
print("Building imports...")
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


def ShowResult():
    print("\nShowing result. Ctrl + C to quit")
    env = make_vec_env(environment_name, seed=1, n_envs=1)
    obs = env.reset()
    while True:
        action, _state = model.predict(obs, deterministic=False)
        obs, reward, done, info = env.step(action)
        env.render(mode="human")


def TrainModel():
    # get steps to train
    steps = input("\nSteps to train: ")
    if steps == "0" or steps == "":
        return
    else:
        steps = int(steps)

    print("training...")
    model.learn(total_timesteps=steps, reset_num_timesteps=False, progress_bar=True)
    if input("\nsave model (y/n)?") == "y":
        model.save("saves/" + input("Save as: "))
        print("done")


environments = [
    "BipedalWalker-v3",
    "LunarLander-v2",
    "CartPole-v1",
    "Custom-v0",
]
print("\nEnvironment:\n0: Bipedal Walker\n1: Lunar Lander\n2: Cart Pole\n3: Custom")
gym.register(id="Custom-v0", entry_point="custom_env:CustomEnv")
environment_name = environments[int(input("? "))]
env = make_vec_env(environment_name, seed=1, n_envs=4)

if input("\nLoad past model (y/n)?") == "y":
    model = PPO.load("saves/" + input("File Name: "), env)
else:
    print("creating model...")
    model = PPO("MlpPolicy", env, verbose=0, device="auto")

TrainModel()
ShowResult()
