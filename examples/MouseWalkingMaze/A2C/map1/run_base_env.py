import os
import sys
sys.path.append('./')

from env.MouseWalkingMaze.base_env import BaseEnv
from stable_baselines import A2C
from stable_baselines.common.vec_env import  DummyVecEnv
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/MouseWalkingMaze/base/'
model_folder = './models/MouseWalkingMaze/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = ''
model_tag = ''
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

env = DummyVecEnv([lambda: BaseEnv(map_name='map1')])

model = A2C(get_policy(policy), env, verbose=0, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=2500000, tb_log_name='A2C_map1' + model_tag)

model.save(model_folder + "A2C_map1" + model_tag)
del model
model = A2C.load(model_folder + "A2C_map1" + model_tag)

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
