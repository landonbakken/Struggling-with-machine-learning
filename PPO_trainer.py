import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Parallel environments
vec_env = make_vec_env("BipedalWalker-v3", seed=1, n_envs=4)

# model = PPO.load("lunar_ppo_1000000.zip", env=vec_env)
model = PPO("MlpPolicy", vec_env, verbose=1, device="auto")
model.learn(total_timesteps=1000000)
model.save("walker_ppo_1000000")

# del model  # remove to demonstrate saving and loading


obs = vec_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render("human")
