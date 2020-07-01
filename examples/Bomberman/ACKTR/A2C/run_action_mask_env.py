import os
import sys
sys.path.append('./')

from env.Bomberman.action_mask_env import ActionMaskEnv
from stable_baselines import ACKTR
from stable_baselines.common.vec_env import  DummyVecEnv, VecFrameStack
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/Bomberman/action_mask/'
model_folder = './models/Bomberman/action_mask/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = ''
model_tag = ''
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

env = DummyVecEnv([lambda: ActionMaskEnv()])
# env = VecFrameStack(env, 2)

model = ACKTR(get_policy(policy), env, verbose=0, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=2500000, tb_log_name='ACKTR_A2C' + model_tag)

model.save(model_folder + "ACKTR_A2C" + model_tag)
del model
model = ACKTR.load(model_folder + "ACKTR_A2C" + model_tag)

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
