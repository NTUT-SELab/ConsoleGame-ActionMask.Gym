import os
import sys
sys.path.append('./')

from env.MouseWalkingMaze.action_mask_env import ActionMaskEnv
from examples.MouseWalkingMaze.map1.custom_policy import CustomCnnLnLstmPolicy
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy

tensorboard_folder = './tensorboard/action_mask/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)

env = DummyVecEnv([lambda: ActionMaskEnv(map_name='map1')])

model = PPO2(CustomCnnLnLstmPolicy, env, verbose=0, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=2500000)

model.save("mouse_action_mask")
del model
model = PPO2.load("mouse_action_mask")

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
