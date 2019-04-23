from gym.envs.registration import register

register(
    id='pro-v0',
    entry_point='gym_foo.envs:FooEnv',
)
