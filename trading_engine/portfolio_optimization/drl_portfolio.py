import gym
from stable_baselines3 import PPO
import numpy as np
import pandas as pd

class PortfolioEnv(gym.Env):
    def __init__(self, data):
        super(PortfolioEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = gym.spaces.Box(low=0, high=1, shape=(len(data.columns),), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(data.columns),), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self._get_observation()

    def step(self, action):
        # Normalize action to ensure it sums to 1 (portfolio weights)
        action_sum = np.sum(action)
        if action_sum == 0:
            action = np.ones_like(action) / len(action)  # Default to equal weights if action is all zeros
        else:
            action = action / action_sum
        
        reward = self._calculate_reward(action)
        self.current_step += 1
        done = self.current_step >= len(self.data) - 1
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        return self.data.iloc[self.current_step].values

    def _calculate_reward(self, action):
        # Calculate portfolio value based on the action (weights) and the next step's returns
        next_returns = self.data.iloc[self.current_step + 1].values
        portfolio_return = np.dot(action, next_returns)  # Expected return based on weights
        return portfolio_return  # Reward is the portfolio return

def train_drl_portfolio(data):
    env = PortfolioEnv(data)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    return model

# Example usage
if __name__ == "__main__":
    asset_type = input("Enter asset type (stocks, cryptocurrencies, forex): ").strip().lower()
    
    # Load returns data based on asset type
    if asset_type == "stocks":
        data = pd.read_csv("data/stock_returns.csv", index_col=0)  # Use the first column as index
    elif asset_type == "cryptocurrencies":
        data = pd.read_csv("data/crypto_data.csv", parse_dates=['Date'], index_col='Date')  # Use the Date column as index
        data = data[['Close']].pct_change().dropna()  # Calculate returns from Close prices
    elif asset_type == "forex":
        data = pd.read_csv("data/forex_data.csv", parse_dates=['Date'], index_col='Date')  # Use the Date column as index
        data = data[['Close']].pct_change().dropna()  # Calculate returns from Close prices
    else:
        raise ValueError("Unsupported asset type")

    # Convert all columns to numeric, forcing errors to NaN
    data = data.apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values
    data = data.dropna()

    # Train the DRL model
    model = train_drl_portfolio(data)
    model.save("models/drl_portfolio")