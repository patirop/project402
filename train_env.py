from spinup import ppo
from spinup import ddpg
import tensorflow as tf
import gym
import gym_foo
# env = gym.make('foo-v0')

env_fn = lambda : gym.make('pro-v0')

logger_kwargs = dict(output_dir='./output', exp_name='experiment_name')

ddpg(env_fn=env_fn,  seed=0,
        steps_per_epoch=5000, epochs=15, replay_size=int(1e6), gamma=0.99,
        polyak=0.995, pi_lr=1e-3, q_lr=1e-3, batch_size=100, start_steps=10000,
        act_noise=0.1, max_ep_len=1000, logger_kwargs=logger_kwargs, save_freq=1)