import numpy as np
import pandas as pd
from scipy.optimize import minimize

def optimize_portfolio(returns):
    """
    Optimize portfolio weights using Markowitz Modern Portfolio Theory (MPT).
    
    Parameters:
    - returns: DataFrame of asset returns.

    Returns:
    - Optimal weights for the portfolio.
    """
    n_assets = len(returns.columns)
    args = (returns.mean(), returns.cov())
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Weights must sum to 1
    bounds = tuple((0, 1) for _ in range(n_assets))  # Weights must be between 0 and 1

    # Minimize portfolio risk
    result = minimize(_portfolio_risk, n_assets * [1. / n_assets], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x

def _portfolio_risk(weights, mean_returns, cov_matrix):
    """
    Calculate the portfolio risk (standard deviation).
    
    Parameters:
    - weights: Portfolio weights.
    - mean_returns: Mean returns of the assets.
    - cov_matrix: Covariance matrix of the asset returns.

    Returns:
    - Portfolio risk.
    """
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def calculate_expected_return(weights, mean_returns):
    """
    Calculate the expected return of the portfolio.
    
    Parameters:
    - weights: Portfolio weights.
    - mean_returns: Mean returns of the assets.

    Returns:
    - Expected return of the portfolio.
    """
    return np.dot(weights, mean_returns)

def calculate_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    """
    Calculate the Sharpe Ratio of the portfolio.
    
    Parameters:
    - weights: Portfolio weights.
    - mean_returns: Mean returns of the assets.
    - cov_matrix: Covariance matrix of the asset returns.
    - risk_free_rate: Risk-free rate.

    Returns:
    - Sharpe Ratio.
    """
    portfolio_return = calculate_expected_return(weights, mean_returns)
    portfolio_risk = _portfolio_risk(weights, mean_returns, cov_matrix)
    return (portfolio_return - risk_free_rate) / portfolio_risk

# Example usage
if __name__ == "__main__":
    asset_type = input("Enter asset type (stocks, cryptocurrencies, forex): ").strip().lower()
    
    # Load returns data based on asset type
    if asset_type == "stocks":
        returns = pd.read_csv("data/stock_returns.csv", index_col=0)  # Use the first column as index
    elif asset_type == "cryptocurrencies":
        returns = pd.read_csv("data/crypto_data.csv", parse_dates=['Date'], index_col='Date')  # Use the Date column as index
        returns = returns[['Close']].pct_change().dropna()  # Calculate returns from Close prices
    elif asset_type == "forex":
        returns = pd.read_csv("data/forex_data.csv", parse_dates=['Date'], index_col='Date')  # Use the Date column as index
        returns = returns[['Close']].pct_change().dropna()  # Calculate returns from Close prices
    else:
        raise ValueError("Unsupported asset type")

    # Convert all columns to numeric, forcing errors to NaN
    returns = returns.apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values
    returns = returns.dropna()

    # Optimize portfolio
    weights = optimize_portfolio(returns)

    # Calculate expected return and Sharpe Ratio
    expected_return = calculate_expected_return(weights, returns.mean())
    sharpe_ratio = calculate_sharpe_ratio(weights, returns.mean(), returns.cov())

    # Output results
    print(f"Optimal Weights: {weights}")
    print(f"Expected Portfolio Return: {expected_return}")
    print(f"Sharpe Ratio: {sharpe_ratio}")