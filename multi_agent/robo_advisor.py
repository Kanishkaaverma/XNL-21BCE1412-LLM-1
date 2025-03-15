import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def robo_advisor(risk_score, investment_goals):
    if risk_score > 70:  # High risk
        advice = "Consider low-risk investments like bonds and index funds."
    elif risk_score > 30:  # Moderate risk
        advice = "Diversify your portfolio with a mix of stocks and ETFs."
    else:  # Low risk
        advice = "Invest in high-growth stocks and emerging markets."
    
    logging.info(f"Robo-Advisor Advice: {advice} based on risk score: {risk_score} and goals: {investment_goals}")
    return advice

# Example usage
if __name__ == "__main__":
    try:
        risk_score = float(input("Enter your risk score (0-100): "))  # Dynamic input for risk score
        investment_goals = input("Enter your investment goals: ")  # Dynamic input for investment goals
        advice = robo_advisor(risk_score, investment_goals)
        print(f"Robo-Advisor Advice: {advice}")
    except ValueError:
        print("Invalid input. Please enter a numeric value for the risk score.")