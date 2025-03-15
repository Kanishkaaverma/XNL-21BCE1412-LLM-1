import pandas as pd
import logging
from anomaly_detection.anomaly_detector import detect_anomalies

# Set up logging
logging.basicConfig(level=logging.INFO, filename='transaction_monitor.log', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_transactions():
    try:
        # Load transaction data
        transactions = pd.read_csv("data/transaction_logs/trade_transactions.csv")
        logging.info("Loaded transaction data successfully.")

        # Detect anomalies
        anomalies = detect_anomalies(transactions)
        
        if anomalies.empty:
            logging.info("No anomalies detected.")
        else:
            for index, row in anomalies.iterrows():
                logging.warning(f"Anomaly Detected: {row.to_dict()}")
                print(f"Anomaly Detected: {row.to_dict()}")  # Optional: Print to console for immediate feedback

    except Exception as e:
        logging.error(f"Error monitoring transactions: {e}")

# Example usage
if __name__ == "__main__":
    monitor_transactions()