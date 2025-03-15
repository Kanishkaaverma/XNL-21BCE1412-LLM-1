from fastapi import APIRouter, Depends, HTTPException
from ..utils.auth_utils import get_current_user
from datetime import datetime, timedelta
import random
import requests

router = APIRouter()

def get_hardcoded_data():
    """
    Fallback hardcoded data in case the API fails or returns empty data.
    """
    labels = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)][::-1]
    prices = [random.randint(100, 200) for _ in range(7)]
    return {
        "chartData": {
            "labels": labels,
            "prices": prices,
        }
    }

@router.get("/market-sentiment")
async def get_market_sentiment(current_user: dict = Depends(get_current_user)):
    """
    Fetch market sentiment data from an external API or return hardcoded data if the API fails.
    """
    try:
        # Example: Fetch real data from Alpha Vantage
        API_KEY = "your_alpha_vantage_api_key"
        SYMBOL = "AAPL"  # Example: Apple Inc.
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check if the API returned valid data
        if "Time Series (Daily)" not in data:
            raise ValueError("Invalid API response")

        # Extract time series data
        time_series = data["Time Series (Daily)"]
        labels = list(time_series.keys())[:7]  # Last 7 days
        prices = [float(time_series[date]["4. close"]) for date in labels]

        return {
            "sentiment": {
                "chartData": {
                    "labels": labels,
                    "prices": prices,
                }
            }
        }
    except Exception as e:
        # Log the error and return hardcoded data
        print(f"Error fetching market sentiment data: {e}")
        return {
            "sentiment": {
                "chartData": get_hardcoded_data()
            }
        }

@router.get("/portfolio")
async def get_portfolio(current_user: dict = Depends(get_current_user)):
    """
    Fetch portfolio data for the authenticated user.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Mock portfolio data
    portfolio = [
        {"symbol": "AAPL", "quantity": 10, "price": 150},
        {"symbol": "GOOGL", "quantity": 5, "price": 2800},
    ]
    return {"portfolio": portfolio}