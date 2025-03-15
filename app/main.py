from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from trading_engine.reinforcement_learning.rl_trader import train_rl_trader
from trading_engine.multi_asset_trading.stock_trader import execute_trade, fetch_data
from trading_engine.portfolio_optimization.markowitz_mpt import optimize_portfolio

app = FastAPI()

# Define request models
class StockTradeRequest(BaseModel):
    asset_type: str  # Add asset_type to the request model
    ticker: str
    action: str

class OptimizePortfolioRequest(BaseModel):
    returns_file: str

@app.post("/train-rl-trader")
async def train_rl_trader_endpoint():
    try:
        # Load historical data
        data = pd.read_csv("data/stock_data.csv")
        print("Loaded data:")
        print(data.head())  # Print the first few rows for debugging

        # Convert relevant columns to numeric, coercing errors to NaN
        data['Open'] = pd.to_numeric(data['Open'], errors='coerce')
        data['High'] = pd.to_numeric(data['High'], errors='coerce')
        data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
        data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
        data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')

        # Drop rows with NaN values
        data = data.dropna()

        # Train the RL trader
        model = train_rl_trader(data)
        model.save("models/rl_trader")
        return {"message": "RL Trader trained successfully"}
    except Exception as e:
        print(f"Error: {e}")  # Log the error to the console
        return {"error": str(e)}  # Return the error message for debugging


@app.post("/execute-stock-trade")
async def execute_stock_trade_endpoint(request: StockTradeRequest):
    try:
        # Call the execute_trade function with the correct parameters
        execute_trade(request.asset_type, request.ticker, request.action)
        return {"message": f"Executed {request.action} trade for {request.ticker} ({request.asset_type})"}
    except Exception as e:
        return {"error": str(e)}  # Return the error message for debugging
    
@app.post("/optimize-portfolio")
async def optimize_portfolio_endpoint(request: OptimizePortfolioRequest):
    try:
        # Load returns data from the specified file
        returns = pd.read_csv(request.returns_file)
        
        # Convert all columns to numeric, forcing errors to NaN
        returns = returns.apply(pd.to_numeric, errors='coerce')

        # Drop rows with NaN values
        returns = returns.dropna()

        if returns.empty:
            return {"error": "The returns data is empty after cleaning."}

        # Optimize portfolio
        weights = optimize_portfolio(returns)

        # Calculate expected return and Sharpe Ratio
        expected_return = calculate_expected_return(weights, returns.mean())
        sharpe_ratio = calculate_sharpe_ratio(weights, returns.mean(), returns.cov())

        # Return results
        return {
            "optimal_weights": weights.tolist(),
            "expected_return": expected_return,
            "sharpe_ratio": sharpe_ratio
        }
    except Exception as e:
        return {"error": str(e)}  # Return the error message for debugging