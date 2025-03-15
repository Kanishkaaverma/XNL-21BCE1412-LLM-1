import requests
from bs4 import BeautifulSoup
import yfinance as yf
import ccxt
import json

# Function to scrape Bloomberg news headlines
def scrape_bloomberg():
    url = "https://www.bloomberg.com/markets"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.find_all("h1")
        return [h.text.strip() for h in headlines]
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Bloomberg: {e}")
        return []

# Function to fetch stock data using Yahoo Finance
def fetch_stock_data(ticker):
    try:
        stock_data = yf.download(ticker, period="1d", progress=False)
        return stock_data.to_json()
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return None

# Function to fetch cryptocurrency data using Binance API
def fetch_crypto_data(symbol):
    try:
        binance = ccxt.binance()
        ticker = binance.fetch_ticker(symbol)
        return ticker
    except Exception as e:
        print(f"Error fetching crypto data for {symbol}: {e}")
        return None

# Function to fetch forex data using Alpha Vantage API
def fetch_forex_data(from_currency, to_currency, api_key):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forex data: {e}")
        return None

# Function to fetch SEC filings using SEC/EDGAR API
def fetch_sec_filings(ticker):
    url = f"https://data.sec.gov/submissions/CIK{ticker}.json"
    
    # Add a User-Agent header to identify the requestor
    headers = {
        "User-Agent": "YourAppName/1.0 (kanishkaverma2003@gmail.com)"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SEC filings: {e}")
        return None

# Main function to fetch and display all data
def main():
    # Fetch Bloomberg news headlines
    news_headlines = scrape_bloomberg()
    print("Bloomberg News Headlines:")
    for headline in news_headlines:
        print(f"- {headline}")

    # Fetch stock data for Apple (AAPL)
    stock_data = fetch_stock_data("AAPL")
    if stock_data:
        print("\nStock Data (AAPL):")
        print(json.dumps(json.loads(stock_data), indent=2))

    # Fetch cryptocurrency data for BTC/USDT
    crypto_data = fetch_crypto_data("BTC/USDT")
    if crypto_data:
        print("\nCrypto Data (BTC/USDT):")
        print(json.dumps(crypto_data, indent=2))

    # Fetch forex data for USD to EUR
    api_key = "XU0ARGXBQ8J48VUF"  # Replace with your Alpha Vantage API key
    forex_data = fetch_forex_data("USD", "EUR", api_key)
    if forex_data:
        print("\nForex Data (USD/EUR):")
        print(json.dumps(forex_data, indent=2))

    # Fetch SEC filings for Apple (CIK: 0000320193)
    sec_filings = fetch_sec_filings("0000320193")
    if sec_filings:
        print("\nSEC Filings (Apple):")
        print(json.dumps(sec_filings, indent=2))

# Run the main function
if __name__ == "__main__":
    main()