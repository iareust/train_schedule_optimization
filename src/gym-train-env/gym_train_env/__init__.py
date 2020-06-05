from gym.envs.registration import register

register(
    id='train-v0',
    entry_point='gym_train_env.envs:TrainEnv',
)

register(
    id='train-tf-v0',
    entry_point='gym_train_env.envs:TrainEnvTF',
)

register(
    id='train-tf-v1',
    entry_point='gym_train_env.envs:TrainEnvTFv1',
)

register(
    id='train-tf-v2',
    entry_point='gym_train_env.envs:TrainEnvTFv2',
)