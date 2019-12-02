import sys
sys.path.append('./')

from env.negative_reward_env import NegativeRewardEnv
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy, CnnLnLstmPolicy, LstmPolicy

env = DummyVecEnv([lambda: NegativeRewardEnv()])

model = PPO2(MlpLnLstmPolicy, env, verbose=0, nminibatches=1)
model.learn(total_timesteps=25000)

model.save("mouse")
del model
model = PPO2.load("mouse")

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()
