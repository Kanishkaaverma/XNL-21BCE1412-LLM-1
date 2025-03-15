import pandas as pd
from stable_baselines3 import PPO
from trading_engine.reinforcement_learning.rl_trader import TradingEnv, calculate_performance_metrics

def backtest_strategy(data, model):
    env = TradingEnv(data)
    obs = env.reset()
    rewards = []
    total_profit = 0
    current_position = 0  # 1 for holding a position, -1 for shorting, 0 for no position

    for i in range(len(data) - 1):
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        rewards.append(reward)

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

    # Calculate performance metrics
    returns = [r for r in rewards if r != 0]  # Filter out zero rewards for metrics calculation
    sharpe_ratio, sortino_ratio, max_drawdown = calculate_performance_metrics(data, model)

    return total_profit, sharpe_ratio, sortino_ratio, max_drawdown

# Example usage
if __name__ == "__main__":
    # Simulate user input for asset type
    asset_type = input("Enter asset type (stocks, cryptocurrencies, forex): ").strip().lower()
    
    # Load data based on asset type
    if asset_type == "stocks":
        data = pd.read_csv("data/stock_data.csv")
    elif asset_type == "cryptocurrencies":
        data = pd.read_csv("data/crypto_data.csv")
    elif asset_type == "forex":
        data = pd.read_csv("data/forex_data.csv")
    else:
        raise ValueError("Unsupported asset type")

    # Convert columns to numeric
    data['Open'] = pd.to_numeric(data['Open'], errors='coerce')
    data['High'] = pd.to_numeric(data['High'], errors='coerce')
    data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')

    # Drop rows with NaN values
    data = data.dropna()

    model = PPO.load("models/rl_trader")
    total_profit, sharpe_ratio, sortino_ratio, max_drawdown = backtest_strategy(data, model)
    
    print(f"Total Profit: {total_profit:.2f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Sortino Ratio: {sortino_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2f}")