from examples.utils.custom_policy import CustomCnnLnLstmPolicy, CustomCnnLstmPolicy, CustomCnnPolicy
from stable_baselines.common.policies import MlpLnLstmPolicy, MlpLstmPolicy, MlpPolicy

def get_policy(policy):
    if policy == '':
        return eval('MlpPolicy')
    return eval(policy)
