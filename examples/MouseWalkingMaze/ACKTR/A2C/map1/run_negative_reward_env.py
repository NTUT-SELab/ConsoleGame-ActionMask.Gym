import os
import sys
sys.path.append('./')

from env.MouseWalkingMaze.negative_reward_env import NegativeRewardEnv
from stable_baselines import ACKTR
from stable_baselines.common.vec_env import  DummyVecEnv
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/MouseWalkingMaze/negative_reward/'
model_folder = './models/MouseWalkingMaze/negative_reward/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = ''
model_tag = ''
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

env = DummyVecEnv([lambda: NegativeRewardEnv(map_name='map1')])

model = ACKTR(get_policy(policy), env, verbose=0, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=2500000, tb_log_name='ACKTR_A2C_map1' + model_tag)

model.save(model_folder + "ACKTR_A2C_map1" + model_tag)
del model
model = ACKTR.load(model_folder + "ACKTR_A2C_map1" + model_tag)

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
