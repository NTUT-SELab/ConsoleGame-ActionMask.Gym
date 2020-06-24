import os
import sys
sys.path.append('./')

from env.Pacman.base_env import BaseEnv
from stable_baselines import ACKTR
from stable_baselines.common.vec_env import SubprocVecEnv, VecFrameStack
from examples.utils.utils import get_policy

tensorboard_folder = './tensorboard/Pacman/base/'
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
    env = SubprocVecEnv([lambda: BaseEnv() for i in range(4)])
    env = VecFrameStack(env, 3)

    model = ACKTR(get_policy(policy), env, n_steps=100, verbose=0,vf_fisher_coef=0.5 , tensorboard_log=tensorboard_folder, kfac_update=10, n_cpu_tf_sess=2, async_eigen_decomp=False)
    model.learn(total_timesteps=100000000, tb_log_name='ACKTR_A2C' + model_tag)

    model.save(model_folder + "ACKTR_A2C" + model_tag)
    del model
    model = ACKTR.load(model_folder + "ACKTR_A2C" + model_tag)

    done = False
    states = None
    obs = env.reset()

    while not done:
        action, states = model.predict(obs, states)
        obs, _, done, info = env.step(action)
        env.render()
