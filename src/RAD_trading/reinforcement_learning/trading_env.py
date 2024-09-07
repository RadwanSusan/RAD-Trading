# src\RAD_trading\reinforcement_learning\trading_env.py
import gym
import numpy as np
class TradingEnvironment(gym.Env):
    def __init__(self, data, initial_balance=10000, transaction_fee=0.001):
        super(TradingEnvironment, self).__init__()
        self.data = data
        self.initial_balance = initial_balance
        self.transaction_fee = transaction_fee
        self.action_space = gym.spaces.Discrete(3)  # 0: Hold, 1: Buy, 2: Sell
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(len(data.columns) + 2,))
        self.reset()
    def reset(self):
        self.current_step = 0
        self.balance = self.initial_balance
        self.shares_held = 0
        self.asset_value = 0
        self.total_value = self.balance
        return self._next_observation()
    def _next_observation(self):
        obs = self.data.iloc[self.current_step].values
        return np.append(obs, [self.balance, self.shares_held])
    def step(self, action):
        self.current_step += 1
        current_price = self.data.iloc[self.current_step]['close']
        if action == 1:  # Buy
            shares_to_buy = self.balance // current_price
            cost = shares_to_buy * current_price * (1 + self.transaction_fee)
            self.balance -= cost
            self.shares_held += shares_to_buy
        elif action == 2:  # Sell
            proceeds = self.shares_held * current_price * (1 - self.transaction_fee)
            self.balance += proceeds
            self.shares_held = 0
        self.asset_value = self.shares_held * current_price
        self.total_value = self.balance + self.asset_value
        done = self.current_step >= len(self.data) - 1
        reward = self.total_value - self.initial_balance
        return self._next_observation(), reward, done, {}
    def render(self, mode='human'):
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}')
        print(f'Asset value: {self.asset_value}')
        print(f'Total value: {self.total_value}')
