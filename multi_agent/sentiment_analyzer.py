from transformers import pipeline

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_market_sentiment(news_headlines):
    sentiment_scores = []
    for headline in news_headlines:
        try:
            result = sentiment_analyzer(headline)[0]
            sentiment_scores.append(result['score'] if result['label'] == "POSITIVE" else -result['score'])
        except Exception as e:
            print(f"Error analyzing headline '{headline}': {e}")
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    return average_sentiment

# Example usage
if __name__ == "__main__":
    headlines = input("Enter news headlines (comma-separated): ").split(',')
    sentiment = analyze_market_sentiment(headlines)
    print(f"Average Market Sentiment: {sentiment:.2f}")