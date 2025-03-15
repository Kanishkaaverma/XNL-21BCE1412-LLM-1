import yfinance as yf
import pandas as pd

def fetch_data(asset_type, ticker, period="1y"):
    """
    Fetch historical data based on asset type.
    """
    if asset_type == "stocks":
        return yf.download(ticker, period=period, progress=False)
    elif asset_type == "cryptocurrencies":
        # For cryptocurrencies, we can use a different source like Binance or CoinGecko
        # Here, we will use yfinance for simplicity, but you may want to switch to a dedicated crypto API
        return yf.download(ticker + "-USD", period=period, progress=False)  # Append '-USD' for crypto
    elif asset_type == "forex":
        # For forex, we can use the currency pair format
        return yf.download(ticker + "=X", period=period, progress=False)  # Append '=X' for forex pairs
    else:
        raise ValueError("Unsupported asset type")

def execute_trade(asset_type, ticker, action):
    """
    Execute a trade based on the asset type.
    """
    print(f"Executing {action} trade for {ticker} ({asset_type})")

# Example usage
if __name__ == "__main__":
    asset_type = input("Enter asset type (stocks, cryptocurrencies, forex): ").strip().lower()
    ticker = input("Enter the ticker symbol: ").strip().upper()
    
    # Fetch historical data
    data = fetch_data(asset_type, ticker)
    
    # Display the fetched data
    print(data.head())
    
    # Execute a trade
    action = input("Enter action (Buy/Sell): ").strip().capitalize()
    execute_trade(asset_type, ticker, action)