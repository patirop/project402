from spinup import ppo
from spinup import ddpg
import tensorflow as tf
import gym
import gym_foo

env_fn = lambda : gym.make('pro-v0')

logger_kwargs = dict(output_dir='./output', exp_name='ddpg')

ddpg(env_fn=env_fn,  seed=0,
        steps_per_epoch=5000, epochs=15, replay_size=int(1e6), gamma=0.99,
        polyak=0.995, pi_lr=0.001, q_lr=0.001, batch_size=100, start_steps=10000,
        act_noise=0.1, max_ep_len=1000, logger_kwargs=logger_kwargs, save_freq=1)

# ppo(env_fn=env_fn, seed=0, steps_per_epoch=4000, epochs=50, gamma=0.99, clip_ratio=0.2, pi_lr=0.0003, vf_lr=0.001,
#  train_pi_iters=80, train_v_iters=80, lam=0.97, max_ep_len=1000, target_kl=0.01, logger_kwargs=logger_kwargs, save_freq=10)
# env = gym.make('foo-v0')
#ac_kwargs = dict(hidden_sizes=[40,40], activation=tf.nn.relu)        
# ppo(env_fn=env_fn, ac_kwargs=ac_kwargs, steps_per_epoch=5000, epochs=250, logger_kwargs=logger_kwargs)
