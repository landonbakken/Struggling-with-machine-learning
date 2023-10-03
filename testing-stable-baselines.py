print("Importing...")
import gymnasium as gym

from stable_baselines3 import A2C


print("Making environment...")
# gym.register(id="TestEnv-v0", entry_point="custom_env:LunarLander")
env = gym.make("LunarLander-v2", render_mode="rgb_array")
# env = gym.make("CartPole-v1", render_mode="rgb_array")

print("Making model...")
model = A2C("MlpPolicy", env, verbose=1)

print("training...")
model.learn(total_timesteps=100000)

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render("human")
    # VecEnv resets automatically
    # if done:
    #   obs = vec_env.reset()
