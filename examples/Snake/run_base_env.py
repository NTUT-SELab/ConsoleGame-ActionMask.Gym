import os
import sys
sys.path.append('./')

from env.Snake.base_env import BaseEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv, VecFrameStack
from stable_baselines.common.policies import MlpPolicy
from examples.MouseWalkingMaze.map1.custom_policy import CustomCnnLnLstmPolicy

tensorboard_folder = './tensorboard/Snake/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)

env = DummyVecEnv([lambda: BaseEnv(10, 10)])
env = VecFrameStack(env, n_stack=3)

model = PPO2(MlpPolicy, env, verbose=0, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=25000000)

model.save("snake_base")
del model
model = PPO2.load("snake_base")

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
