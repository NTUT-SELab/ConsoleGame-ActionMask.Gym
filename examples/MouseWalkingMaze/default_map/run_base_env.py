import os
import sys
sys.path.append('./')

from env.MouseWalkingMaze.base_env import BaseEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy

tensorboard_folder = './tensorboard/MouseWalkingMaze/base/'
model_folder = './models/MouseWalkingMaze/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

env = DummyVecEnv([lambda: BaseEnv()])

model = PPO2(MlpLnLstmPolicy, env, verbose=0, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=25000)

model_tag = ''
if len(sys.argv) > 1:
    model_tag = '_' + sys.argv[1]

model.save(model_folder + "PPO2_MlpLnLstm" + model_tag)
del model
model = PPO2.load(model_folder + "PPO2_MlpLnLstm" + model_tag)

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
