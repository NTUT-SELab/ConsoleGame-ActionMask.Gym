import os
import sys
sys.path.append('./')

from env.negative_reward_env import NegativeRewardEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy

tensorboard_folder = './tensorboard/negative_reward/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)

env = DummyVecEnv([lambda: NegativeRewardEnv()])

model = PPO2(MlpLnLstmPolicy, env, verbose=0, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=25000)

model.save("mouse_negative_reward")
del model
model = PPO2.load("mouse_negative_reward")

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
