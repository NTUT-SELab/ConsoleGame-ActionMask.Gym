import sys
sys.path.append('./')

from env.action_mask_env import ActionMaskEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy, CnnLnLstmPolicy, LstmPolicy

env = DummyVecEnv([lambda: ActionMaskEnv()])

model = PPO2(MlpLnLstmPolicy, env, verbose=0, nminibatches=1)
model.learn(total_timesteps=25000)

model.save("mouse")
del model
model = PPO2.load("mouse")

done = False
states = None
action_mask = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states, action_mask)
    obs, _, done, info = env.step(action)
    action_mask = info.get('action_mask')
    env.render()
