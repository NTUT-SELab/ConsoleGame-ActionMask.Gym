import os
import sys
sys.path.append('./')

from env.Bomberman.base_env import BaseEnv
from stable_baselines import DQN
from stable_baselines.common.vec_env import  DummyVecEnv, VecFrameStack
from stable_baselines.deepq.policies import CnnPolicy
from examples.utils.custom_policy import modified_cnn

class CustomCnnPolicy(CnnPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch,
                 reuse=False, obs_phs=None, dueling=True, **_kwargs):
        super(CnnPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                        feature_extraction="cnn", obs_phs=obs_phs, dueling=dueling,
                                        layer_norm=False, cnn_extractor=modified_cnn, **_kwargs)

tensorboard_folder = './tensorboard/Bomberman/base/'
model_folder = './models/Bomberman/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)
if not os.path.isdir(model_folder):
    os.makedirs(model_folder)

policy = 'Cnn'
model_tag = 'Cnn'
if len(sys.argv) > 1:
    policy = sys.argv[1]
    model_tag = '_' + sys.argv[1]

env = DummyVecEnv([lambda: BaseEnv()])
env = VecFrameStack(env, 2)

model = DQN(CustomCnnPolicy, env, verbose=0, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=10000000, tb_log_name='DQN' + model_tag)

model.save(model_folder + "DQN" + model_tag)
del model
model = DQN.load(model_folder + "DQN" + model_tag)

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()