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
from stable_baselines3.common.env_checker import check_env
from pettingzoo.classic import tictactoe_v3
from custom_env import CustomEnv


def ShowResult():
    print("\nShowing result. Ctrl + C to quit")
    env = make_vec_env(environment_name, seed=1, n_envs=1)
    obs = env.reset()
    while True:
        action, _state = model.predict(obs, deterministic=True)
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
    "Custom-v0",
    "TicTacToe-v3",
]
print(
    "\nEnvironment:\n0: Bipedal Walker\n1: Lunar Lander\n2: Cart Pole\n3: Custom\n4: Check Custom\n5: Tic Tac Toe"
)
option = int(input("? "))
environment_name = environments[option]
if environment_name == "TicTacToe-v3":
    env = tictactoe_v3.env(render_mode="human")
else:
    if environment_name == "Custom-v0":
        gym.register(id="Custom-v0", entry_point="custom_env:CustomEnv")

    env = gym.make(
        environment_name,
    )  # make_vec_env(environment_name, seed=1, n_envs=4)
if option == 4:
    check_env(env)
    print("Custom env is valid (:")
    exit()

if input("\nLoad past model (y/n)?") == "y":
    model = PPO.load("saves/" + input("File Name: "), env)
else:
    print("creating model...")
    model = PPO("MlpPolicy", env, verbose=0, device="auto")

TrainModel()
ShowResult()
