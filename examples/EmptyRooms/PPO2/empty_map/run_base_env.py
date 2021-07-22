import os
import sys
sys.path.append('./')

from env.EmptyRooms.base_env import BaseEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/EmptyRooms/base/'
model_folder = './models/EmptyRooms/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = ''
model_tag = ''
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

env = DummyVecEnv([lambda: BaseEnv()])

model = PPO2(get_policy(policy), env, verbose=1, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=1000000, tb_log_name='PPO2' + model_tag)

model.save(model_folder + "PPO2" + model_tag)


