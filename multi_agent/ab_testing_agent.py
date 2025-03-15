from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Example model classes
class ModelA:
    def fit(self, X, y):
        # Dummy fit method
        pass

    def predict(self, X):
        # Dummy predict method
        return [1] * len(X)  # Example prediction

class ModelB:
    def fit(self, X, y):
        # Dummy fit method
        pass

    def predict(self, X):
        # Dummy predict method
        return [0] * len(X)  # Example prediction

def evaluate_model(model, data, labels):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted', zero_division=0)
    recall = recall_score(y_test, predictions, average='weighted', zero_division=0)
    f1 = f1_score(y_test, predictions, average='weighted', zero_division=0)
    
    return accuracy, precision, recall, f1

# Example usage
if __name__ == "__main__":
    # Dummy data and labels
    data = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]  # Example feature data
    labels = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # Example target labels
    
    accuracy_a, precision_a, recall_a, f1_a = evaluate_model(ModelA(), data, labels)
    accuracy_b, precision_b, recall_b, f1_b = evaluate_model(ModelB(), data, labels)
    
    print(f"Model A - Accuracy: {accuracy_a}, Precision: {precision_a}, Recall: {recall_a}, F1: {f1_a}")
    print(f"Model B - Accuracy: {accuracy_b}, Precision: {precision_b}, Recall: {recall_b}, F1: {f1_b}")