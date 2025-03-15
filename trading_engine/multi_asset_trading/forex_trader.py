import requests
import pandas as pd

def fetch_forex_data(from_currency, to_currency, api_key):
    """
    Fetch historical forex data from Alpha Vantage.
    """
    url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_currency}&to_symbol={to_currency}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    # Check for errors in the response
    if "Error Message" in data:
        raise ValueError(data["Error Message"])
    
    # Convert the response to a DataFrame
    df = pd.DataFrame(data['Time Series FX (Daily)']).T
    df.columns = ['open', 'high', 'low', 'close']  # Only four columns for forex data
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)  # Convert to float
    return df

def execute_trade(asset_type, pair, action):
    """
    Execute a trade based on the asset type.
    """
    print(f"Executing {action} trade for {pair} ({asset_type})")

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your actual API key
    from_currency = input("Enter the base currency (e.g., USD): ").strip().upper()
    to_currency = input("Enter the target currency (e.g., EUR): ").strip().upper()
    
    # Fetch historical data
    data = fetch_forex_data(from_currency, to_currency, api_key)
    
    # Display the fetched data
    print(data.head())
    
    # Execute a trade
    action = input("Enter action (Buy/Sell): ").strip().capitalize()
    execute_trade("forex", f"{from_currency}/{to_currency}", action)