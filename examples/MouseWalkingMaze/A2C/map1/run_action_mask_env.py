import os
import sys
sys.path.append('./')

from env.MouseWalkingMaze.action_mask_env import ActionMaskEnv
from stable_baselines import A2C
from stable_baselines.common.vec_env import  DummyVecEnv
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/MouseWalkingMaze/action_mask/'
model_folder = './models/MouseWalkingMaze/action_mask/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = ''
model_tag = ''
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

env = DummyVecEnv([lambda: ActionMaskEnv(map_name='map1')])

model = A2C(get_policy(policy), env, verbose=0, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=2500000, tb_log_name='A2C_map1' + model_tag)

model.save(model_folder + "A2C_map1" + policy)
del model
model = A2C.load(model_folder + "A2C_map1" + policy)

done = False
states = None
action_masks = []
obs = env.reset()

while not done:
    action, states = model.predict(obs, states, action_mask=action_masks)
    obs, _, done, infos = env.step(action)
    env.render()
    action_masks.clear()
    for info in infos:
            env_action_mask = info.get('action_mask')
            action_masks.append(env_action_mask) 
