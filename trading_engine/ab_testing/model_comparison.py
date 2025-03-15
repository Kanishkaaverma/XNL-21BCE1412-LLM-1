import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor # type: ignore
from xgboost import XGBRegressor # type: ignore
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from keras.models import Sequential # type: ignore
from keras.layers import LSTM, Dense # type: ignore
import yfinance as yf  # For stocks and cryptocurrencies # type: ignore
import time

def fetch_real_time_data(ticker):
    # Fetch real-time data using yfinance
    data = yf.download(ticker, period='1d', interval='1m')  # Adjust as needed
    return data

def make_predictions(trained_models, latest_data):
    predictions = {}
    # Rename columns to match training data
    latest_data.columns = ['Open', 'High', 'Low', 'Volume']
    
    for name, model in trained_models.items():
        if name == "LSTM":
            # Reshape latest data for LSTM
            latest_data_lstm = latest_data.values.reshape((1, latest_data.shape[1], 1))
            predictions[name] = model.predict(latest_data_lstm)
        else:
            predictions[name] = model.predict(latest_data)
    return predictions

def compare_models(X_train, y_train, X_test, y_test):
    models = {
        "XGBoost": XGBRegressor(),
        "LSTM": create_lstm_model(X_train),
    }
    
    results = {}
    trained_models = {}  # Dictionary to store trained models
    for name, model in models.items():
        if name == "LSTM":
            # Reshape data for LSTM
            X_train_lstm = X_train.values.reshape((X_train.shape[0], X_train.shape[1], 1))
            model.fit(X_train_lstm, y_train, epochs=10, batch_size=32)
            y_pred = model.predict(X_test.values.reshape((X_test.shape[0], X_test.shape[1], 1)))
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            "MSE": mse,
            "MAE": mae,
            "R2": r2
        }
        trained_models[name] = model  # Store the trained model

    return results, trained_models  # Return both results and trained models

def create_lstm_model(X_train):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def auto_select_best_model(results):
    # Implement logic to select the best model based on criteria
    best_model = min(results, key=lambda x: results[x]['MSE'])  # Example: select based on MSE
    return best_model

# Example usage
if __name__ == "__main__":
    # User input for asset type and ticker
    asset_type = input("Enter asset type (stock, crypto, forex): ").strip().lower()
    ticker = input("Enter the ticker symbol (e.g., AAPL for stocks, BTC-USD for crypto, EURUSD=X for forex): ").strip()

    # Load historical data
    data = pd.read_csv("data/stock_data.csv", header=0, index_col=0)  # Use the first column as index
    
    # Print the first few rows of the data for debugging
    print("Loaded data:")
    print(data.head())
    
    # Rename columns to match expected format
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Convert relevant columns to numeric
    data = data.apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with NaN values
    data = data.dropna()
    
    # Print the shape of the data after dropping NaNs
    print(f"Data shape after dropping NaNs: {data.shape}")
    
    # Feature selection
    X = data[['Open', 'High', 'Low', 'Volume']]
    y = data['Close']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Check for NaN values after splitting
    if X_train.isnull().values.any() or y_train.isnull().values.any():
        print("Warning: NaN values found in training features or target variable. Exiting...")
        exit(1)
    
    # Compare models
    results, trained_models = compare_models(X_train, y_train, X_test, y_test)
    
    # Print results
    print("Model Comparison Results:")
    for model_name, metrics in results.items():
        print(f"{model_name}: MSE={metrics['MSE']:.4f}, MAE={metrics['MAE']:.4f}, R2={metrics['R2']:.4f}")
    
    # Auto-select best model
    best_model = auto_select_best_model(results)
    print(f"Best Model: {best_model}")
    
    # Real-time prediction loop
    max_iterations = 100  # Limit the number of iterations
    iteration_count = 0
    start_time = time.time()
    max_duration = 3600  # Run for a maximum of 1 hour (3600 seconds)

    while iteration_count < max_iterations and (time.time() - start_time) < max_duration:
        latest_data = fetch_real_time_data(ticker)
        if not latest_data.empty:
            # Prepare latest data for prediction
            latest_features = latest_data[['Open', 'High', 'Low', 'Volume']].tail(1)  # Get the latest row
            predictions = make_predictions(trained_models, latest_features)
            print(f"Latest Predictions: {predictions}")
        
        # Sleep for a while before fetching new data
        time.sleep(60)  # Adjust the sleep time as needed
        iteration_count += 1  # Increment the iteration count

    print("Real-time prediction loop has ended.")