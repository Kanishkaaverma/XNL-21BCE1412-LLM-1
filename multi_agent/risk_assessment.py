from transformers import pipeline
import numpy as np
from scipy.stats import norm
import yfinance as yf

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to calculate risk score based on sentiment analysis
def calculate_risk_score(text):
    try:
        sentiment_result = sentiment_analyzer(text)[0]
        sentiment_label = sentiment_result['label']
        sentiment_score = sentiment_result['score']
        
        if sentiment_label == "NEGATIVE":
            risk_score = sentiment_score * 100  # Higher risk for negative sentiment
        else:
            risk_score = (1 - sentiment_score) * 100  # Lower risk for positive sentiment
        
        return risk_score
    except Exception as e:
        print(f"Error calculating risk score: {e}")
        return None

# Function to calculate volatility using historical stock prices
def calculate_volatility(prices):
    try:
        returns = np.diff(prices) / prices[:-1]  # Calculate daily returns
        volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
        return volatility
    except Exception as e:
        print(f"Error calculating volatility: {e}")
        return None

# Function to calculate Value at Risk (VaR) using historical stock prices
def calculate_var(prices, confidence_level=0.95):
    try:
        returns = np.diff(prices) / prices[:-1]  # Calculate daily returns
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        var = norm.ppf(1 - confidence_level, mean_return, std_return)
        return var
    except Exception as e:
        print(f"Error calculating VaR: {e}")
        return None

# Function to fetch historical stock prices using Yahoo Finance
def fetch_stock_prices(ticker, period="1y"):
    try:
        stock_data = yf.download(ticker, period=period, progress=False)
        prices = stock_data['Close'].values.flatten()  # Flatten to 1D array
        print(f"Fetched prices for {ticker}: {prices}")  # Debugging line
        return prices
    except Exception as e:
        print(f"Error fetching stock prices for {ticker}: {e}")
        return None

# Main function to demonstrate risk assessment
def main():
    # Example text for sentiment analysis
    text = "The stock market is crashing due to global economic concerns."
    
    # Calculate risk score
    risk_score = calculate_risk_score(text)
    if risk_score is not None:
        print(f"Risk Score: {risk_score:.2f}")

    # Fetch historical stock prices for Apple (AAPL)
    ticker = "AAPL"
    prices = fetch_stock_prices(ticker)
    if prices is not None and len(prices) > 0:
        print(f"Prices shape: {prices.shape}")  # Debugging line

        # Calculate volatility
        volatility = calculate_volatility(prices)
        if volatility is not None:
            print(f"Annualized Volatility ({ticker}): {volatility:.4f}")

        # Calculate Value at Risk (VaR)
        var = calculate_var(prices)
        if var is not None:
            print(f"Value at Risk (95% confidence, {ticker}): {var:.4f}")
    else:
        print(f"No valid prices fetched for {ticker}.")

# Run the main function
if __name__ == "__main__":
    main()