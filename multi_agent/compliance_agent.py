def compliance_check(transaction):
    # Example compliance rules
    if transaction["amount"] > 10000:  # Large transaction
        return "Flagged for review"
    else:
        return "Compliant"

# Example usage
if __name__ == "__main__":
    amount = float(input("Enter transaction amount: "))
    transaction = {"amount": amount, "description": "Sample transaction"}
    compliance_status = compliance_check(transaction)
    print(f"Compliance Status: {compliance_status}")