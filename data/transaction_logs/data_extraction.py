import ccxt
import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta

# Initialize Binance API
binance = ccxt.binance()

# Fetch recent trades for BTC/USDT
trades = binance.fetch_trades("BTC/USDT", limit=1000)

# Convert to DataFrame
trade_data = []
for trade in trades:
    trade_data.append({
        "transaction_id": trade['id'],
        "timestamp": trade['datetime'],
        "asset_type": "crypto",
        "asset_name": trade['symbol'],
        "amount": trade['amount'],
        "price": trade['price'],
        "description": f"{trade['side']} {trade['symbol']}"
    })

trade_transactions = pd.DataFrame(trade_data)
trade_transactions.to_csv("data/transaction_logs/trade_transactions.csv", index=False)

# Replace with your Alpha Vantage API key
api_key = "XUOARGXBQ8J48VUF"

# Fetch stock trades for AAPL
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=1min&apikey={api_key}"
response = requests.get(url)
data = response.json()

# Check if the expected key exists
if 'Time Series (1min)' in data:
    trade_data = []
    for timestamp, values in data['Time Series (1min)'].items():
        trade_data.append({
            "transaction_id": f"TX{timestamp}",
            "timestamp": timestamp,
            "asset_type": "stock",
            "asset_name": "AAPL",
            "amount": float(values['4. close']),
            "price": float(values['1. open']),
            "description": f"Stock trade for AAPL at {timestamp}"
        })
    trade_transactions = pd.DataFrame(trade_data)
    trade_transactions.to_csv("data/transaction_logs/trade_transactions.csv", index=False)
else:
    print("Error fetching stock trades:", data)

# Fetch forex trades for USD/EUR
url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=EUR&interval=1min&apikey={api_key}"
response = requests.get(url)
data = response.json()

# Check if the expected key exists
if 'Time Series FX (1min)' in data:
    trade_data = []
    for timestamp, values in data['Time Series FX (1min)'].items():
        trade_data.append({
            "transaction_id": f"TX{timestamp}",
            "timestamp": timestamp,
            "asset_type": "forex",
            "asset_name": "USD/EUR",
            "amount": float(values['4. close']),
            "price": float(values['1. open']),
            "description": f"Forex trade for USD/EUR at {timestamp}"
        })
    trade_transactions = pd.DataFrame(trade_data)
    trade_transactions.to_csv("data/transaction_logs/trade_transactions.csv", index=False)
else:
    print("Error fetching forex trades:", data)

# Load trade transactions
trade_transactions = pd.read_csv("data/transaction_logs/trade_transactions.csv")

# Generate synthetic compliance checks
def generate_compliance_checks(trade_transactions):
    data = []
    for _, row in trade_transactions.iterrows():
        check_id = f"CHK{row['transaction_id'][2:]}"
        check_type = np.random.choice(["AML", "KYC"])
        status = np.random.choice(["Pass", "Fail"])
        timestamp = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=np.random.randint(1, 60))
        data.append({
            "check_id": check_id,
            "transaction_id": row['transaction_id'],
            "check_type": check_type,
            "status": status,
            "timestamp": timestamp.strftime("%Y-%m-%d %H :%M:%S")
        })
    return pd.DataFrame(data)

# Save to CSV
compliance_checks = generate_compliance_checks(trade_transactions)
compliance_checks.to_csv("data/transaction_logs/compliance_checks.csv", index=False)