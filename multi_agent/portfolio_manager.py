import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def portfolio_manager(risk_score):
    if risk_score > 70:  # High risk
        recommendation = "Invest in bonds and stable assets"
    elif risk_score > 30:  # Moderate risk
        recommendation = "Diversify portfolio with stocks and ETFs"
    else:  # Low risk
        recommendation = "Invest in high-growth stocks"
    
    logging.info(f"Portfolio Recommendation: {recommendation} based on risk score: {risk_score}")
    return recommendation

# Example usage
if __name__ == "__main__":
    risk_score = float(input("Enter risk score: "))  # User input for risk score
    recommendation = portfolio_manager(risk_score)
    print(f"Portfolio Recommendation: {recommendation}")