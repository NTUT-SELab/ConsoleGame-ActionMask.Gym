import os
import sys
sys.path.append('./')

from env.Snake.base_env import BaseEnv
from stable_baselines import A2C
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from examples.MouseWalkingMaze.map1.custom_policy import CustomCnnLnLstmPolicy

tensorboard_folder = './tensorboard/Snake/base/'
model_folder = './models/Snake/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

env = DummyVecEnv([lambda: BaseEnv(10, 10)])

model = A2C(MlpPolicy, env, verbose=0, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=10000000)

model_tag = ''
if len(sys.argv) > 1:
    model_tag = '_' + sys.argv[1]

model.save(model_folder + "A2C" + model_tag)
del model
model = A2C.load(model_folder + "A2C" + model_tag)

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
