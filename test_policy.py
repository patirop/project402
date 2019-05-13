from spinup.utils.test_policy import load_policy, run_policy
import gym
import gym_foo
_, get_action = load_policy('./output')
env = gym.make('pro-v0')
run_policy(env, get_action)