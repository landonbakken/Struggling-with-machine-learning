print("Building imports...")
import gymnasium as gym

from stable_baselines3 import A2C


def ShowResult():
    stepsToShow = int(input("Steps to show (default = 1000): "))
    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(stepsToShow):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        vec_env.render("human")
        # VecEnv resets automatically
        # if done:
        #   obs = vec_env.reset()


def TrainModel():
    steps = int(input("Steps (default = 100000): "))
    print("training...")
    model.learn(total_timesteps=steps, reset_num_timesteps=False)
    if input("save model (y/n)?") == "y":
        model.save(input("Save as: "))
        print("done")


print("Building environment...")
env = gym.make("LunarLander-v2", render_mode="rgb_array")

if input("load model (y/n)?") == "y":
    model = A2C.load(input("File: "), env, tensorboard_log="./tenserboard/")
    if input("Train further (y/n)? ") == "y":
        TrainModel()
    ShowResult()
else:
    print("creating model...")
    model = A2C("MlpPolicy", env, verbose=1, tensorboard_log="./tenserboard/")
    TrainModel()
    ShowResult()


# gym.register(id="TestEnv-v0", entry_point="custom_env:LunarLander")
# env = gym.make("CartPole-v1", render_mode="rgb_array")
