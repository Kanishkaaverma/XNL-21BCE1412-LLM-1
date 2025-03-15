import gym # type: ignore
from stable_baselines3 import PPO  # type: ignore
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    def __init__(self, data):
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(3)  # Buy, Sell, Hold
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self._get_observation()

    def step(self, action):
        reward = self._calculate_reward(action)
        self.current_step += 1
        done = self.current_step >= len(self.data) - 1
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        # Ensure the observation is a float32 array
        return self.data.iloc[self.current_step][['Open', 'High', 'Low', 'Close', 'Volume']].values.astype(np.float32) / 100.0  # Example normalization

    def _calculate_reward(self, action):
        current_price = self.data.iloc[self.current_step]['Close']
        next_price = self.data.iloc[self.current_step + 1]['Close']
        
        if action == 0:  # Buy
            return next_price - current_price  # Reward for buying
        elif action == 1:  # Sell
            return current_price - next_price  # Reward for selling
        else:  # Hold
            return 0  # No reward for holding

def train_rl_trader(data, total_timesteps=10000):
    env = TradingEnv(data)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=total_timesteps)
    return model

def load_data(asset_type):
    if asset_type == "stocks":
        return pd.read_csv("data/stock_data.csv")  # Load historical stock data
    elif asset_type == "cryptocurrencies":
        return pd.read_csv("data/crypto_data.csv")  # Load historical crypto data
    elif asset_type == "forex":
        return pd.read_csv("data/forex_data.csv")  # Load historical forex data
    else:
        raise ValueError("Unsupported asset type")

def calculate_performance_metrics(data, model):
    # Simulate trading
    total_profit = 0
    returns = []
    current_position = 0  # 1 for holding a position, -1 for shorting, 0 for no position

    for i in range(len(data) - 1):
        obs = data.iloc[i][['Open', 'High', 'Low', 'Close', 'Volume']].values.astype(np.float32) / 100.0
        action, _ = model.predict(obs, deterministic=True)

        current_price = data.iloc[i]['Close']
        next_price = data.iloc[i + 1]['Close']

        if action == 0:  # Buy
            current_position = 1
        elif action == 1:  # Sell
            current_position = -1
        else:  # Hold
            current_position = current_position

        if current_position == 1:  # If holding a position
            profit = next_price - current_price
            total_profit += profit
            returns.append(profit / current_price)  # Calculate return

    # Calculate metrics
    returns = np.array(returns)
    sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)  # Annualized Sharpe Ratio
    sortino_ratio = np.mean(returns) / np.std(returns[returns < 0]) * np.sqrt(252)  # Annualized Sortino Ratio
    max_drawdown = calculate_max_drawdown(returns)

    return sharpe_ratio, sortino_ratio, max_drawdown

def calculate_max_drawdown(returns):
    cumulative_returns = np.cumprod(1 + returns) - 1
    peak = np.maximum.accumulate(cumulative_returns)
    drawdown = (peak - cumulative_returns) / peak
    return np.max(drawdown)

# Example usage
if __name__ == "__main__":
    # Simulate user input for asset type
    asset_type = input("Enter asset type (stocks, cryptocurrencies, forex): ").strip().lower()
    
    data = load_data(asset_type)

    # Convert columns to numeric
    data['Open'] = pd.to_numeric(data['Open'], errors='coerce')
    data['High'] = pd.to_numeric(data['High'], errors='coerce')
    data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')

    # Drop rows with NaN values
    data = data.dropna()

    model = train_rl_trader(data)

    # Calculate performance metrics
    sharpe_ratio, sortino_ratio, max_drawdown = calculate_performance_metrics(data, model)
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Sortino Ratio: {sortino_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2f}")

    model.save("models/rl_trader")