import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def trade_execution_ai(sentiment):
    if sentiment > 0.5:  # Positive sentiment
        decision = "Buy"
    elif sentiment < -0.5:  # Negative sentiment
        decision = "Sell"
    else:
        decision = "Hold"
    
    logging.info(f"Trade Decision: {decision} based on sentiment: {sentiment}")
    return decision

# Example usage
if __name__ == "__main__":
    sentiment = float(input("Enter sentiment score: "))  # User input for sentiment
    decision = trade_execution_ai(sentiment)
    print(f"Trade Decision: {decision}")