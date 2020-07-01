import os
import sys
sys.path.append('./')

from env.Pacman.action_mask_env import ActionMaskEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import DummyVecEnv, VecFrameStack
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/Pacman/action_mask/'
model_folder = './models/Pacman/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = ''
model_tag = ''
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

if __name__ == '__main__':
    env = DummyVecEnv([lambda: ActionMaskEnv() for i in range(4)])
    env = VecFrameStack(env, 3)

    model = PPO2.load(model_folder + "PPO2" + model_tag)

    done = [False, False, False, False]
    states = None
    action_masks = []
    obs = env.reset()

    while not done[0]:
        action, states = model.predict(obs, states, action_mask=action_masks)
        obs, _, done, infos = env.step(action)
        env.render()
        action_masks.clear()
        for info in infos:
            env_action_mask = info.get('action_mask')
            action_masks.append(env_action_mask) 
