from kafka import KafkaProducer
import yfinance as yf

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Fetch Stock Data
stock_data = yf.download("AAPL", period="1d")
producer.send('stock-data', stock_data.to_json().encode('utf-8'))