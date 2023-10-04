# get rid of annoying deprecation warnings I can do nothing about
import os
import warnings

warnings.warn = lambda *args, **kwargs: None
os.system("cls")
print("Building imports...")
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


def ShowResult():
    print("Showing result. Ctrl + C to quit")
    env = make_vec_env(environment_name, seed=1, n_envs=1)
    obs = env.reset()
    while True:
        action, _state = model.predict(obs, deterministic=False)
        obs, reward, done, info = env.step(action)
        env.render("human")


def TrainModel():
    # get steps to train
    steps = input("Steps: ")
    if steps == "0" or steps == "":
        return
    else:
        steps = int(steps)

    print("training...")
    model.learn(total_timesteps=steps, reset_num_timesteps=False)
    if input("save model (y/n)?") == "y":
        model.save("saves/" + input("Save as: "))
        print("done")


environments = ["BipedalWalker-v3", "LunarLander-v2", "CartPole-v1"]
print("\nEnvironment:\n0: Bipedal Walker\n1: Lunar Lander\n2: Cart Pole")
environment_name = environments[int(input("? "))]
env = make_vec_env(environment_name, seed=1, n_envs=4)

if input("Load past model (y/n)?") == "y":
    model = PPO.load("saves/" + input("File: "), env)
else:
    print("creating model...")
    model = PPO("MlpPolicy", env, verbose=1, device="auto")

TrainModel()
ShowResult()


# gym.register(id="TestEnv-v0", entry_point="custom_env:LunarLander")
# env = gym.make("CartPole-v1", render_mode="rgb_array")
