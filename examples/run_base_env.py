import os
import sys
sys.path.append('./')

from env.base_env import BaseEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy

tensorboard_folder = './tensorboard/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)

env = DummyVecEnv([lambda: BaseEnv()])

model = PPO2(MlpLnLstmPolicy, env, verbose=0, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=25000)

model.save("mouse_base")
del model
model = PPO2.load("mouse_base")

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
