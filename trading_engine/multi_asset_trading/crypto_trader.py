import ccxt
import pandas as pd

def fetch_crypto_data(symbol, timeframe='1d'):
    """
    Fetch historical cryptocurrency data from Binance.
    """
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe)
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def execute_trade(asset_type, symbol, action):
    """
    Execute a trade based on the asset type.
    """
    print(f"Executing {action} trade for {symbol} ({asset_type})")

# Example usage
if __name__ == "__main__":
    asset_type = "cryptocurrencies"  # This can be dynamic based on user input
    symbol = input("Enter the cryptocurrency symbol (e.g., BTC/USDT): ").strip().upper()
    
    # Fetch historical data
    data = fetch_crypto_data(symbol)
    
    # Display the fetched data
    print(data.head())
    
    # Execute a trade
    action = input("Enter action (Buy/Sell): ").strip().capitalize()
    execute_trade(asset_type, symbol, action)