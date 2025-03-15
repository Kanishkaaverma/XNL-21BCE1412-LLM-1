import pandas as pd
from prophet import Prophet # type: ignore

def predict_market_trend(prices):
    # Ensure prices is a pandas Series with a DateTime index
    if not isinstance(prices, pd.Series):
        raise ValueError("Input prices must be a pandas Series.")

    # Prepare the DataFrame for Prophet
    df = pd.DataFrame({'ds': prices.index, 'y': prices.values})
    
    # Initialize and fit the Prophet model
    model = Prophet()
    model.fit(df)
    
    # Create a DataFrame for future dates
    future = model.make_future_dataframe(periods=365)
    
    # Make predictions
    forecast = model.predict(future)
    
    # Return relevant columns from the forecast
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]