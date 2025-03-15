# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from py2neo import Graph
# from transformers import pipeline
# import time
# from torch_geometric.nn import GCNConv # type: ignore
# from torch_geometric.data import Data # type: ignore

# # Define GNN model
# class FraudDetectionGNN(nn.Module):
#     def __init__(self):
#         super(FraudDetectionGNN, self).__init__()
#         self.conv1 = GCNConv(32, 16)  # First graph convolution layer
#         self.conv2 = GCNConv(16, 8)    # Second graph convolution layer

#     def forward(self, data):
#         x, edge_index = data.x, data.edge_index  # Unpack data
#         x = self.conv1(x, edge_index)  # Apply first convolution
#         x = F.relu(x)                  # Apply ReLU activation
#         x = self.conv2(x, edge_index)  # Apply second convolution
#         return x

# # Load GNN model
# model_path = "/Users/kanishkaverma/Desktop/fintech-llm/models/falcon_gnn_dgl.pth"  # Update this path if needed
# model = FraudDetectionGNN()
# model.load_state_dict(torch.load(model_path))
# model.eval()

# # Connect to Neo4j
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# def fetch_transaction_graph():
#     query = """
#     MATCH (a:Account)-[t:TRANSACTION]->(b:Account)
#     WHERE t.amount > 1000000
#     RETURN a, t, b
#     """
#     result = graph.run(query).data()
    
#     # Debugging: Check the result of the query
#     print("Query result:", result)  # Debugging output

#     if not result:
#         print("No transactions found that meet the criteria.")
#         return None  # Return None if no transactions are found

#     edges = []
#     for record in result:
#         src = int(record['a']['id'])  # Ensure IDs are integers
#         dst = int(record['b']['id'])
#         edges.append((src, dst))
    
#     # Debugging: Check the edges collected
#     print(f"Edges collected: {edges}")

#     if not edges:
#         print("No edges found.")
#         return None  # Return None if no edges are found

#     edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()  # Create edge index tensor
#     x = torch.randn(len(edges), 32)  # Node features (random for example)
    
#     # Create a Data object for PyTorch Geometric
#     data = Data(x=x, edge_index=edge_index)
#     return data

# def detect_anomalies(output, threshold=0.8):
#     """
#     Detect anomalies based on GNN output.
#     """
#     anomalies = output[output > threshold]
#     return anomalies

# def detect_insider_trading(data):
#     alerts = []
#     # Implement logic to detect insider trading
#     return alerts

# def detect_pump_and_dump(data):
#     alerts = []
#     # Implement logic to detect pump & dump schemes
#     return alerts

# def detect_money_laundering(data):
#     alerts = []
#     # Implement logic to detect money laundering
#     return alerts

# # Load LLM for text analysis
# fraud_llm = pipeline("text-classification", model="yiyanghkust/finbert-tone")  # Use a suitable model for fraud detection

# def analyze_transaction_description(description):
#     """
#     Analyze transaction description using LLM.
#     """
#     result = fraud_llm(description)[0]
#     return result['label'], result['score']

# # Set maximum number of iterations
# max_iterations = 10  # Set the maximum number of iterations
# current_iteration = 0

# # Real-time monitoring loop
# while current_iteration < max_iterations:
#     print(f"Iteration {current_iteration + 1} of {max_iterations}")
    
#     # Fetch new transactions
#     data = fetch_transaction_graph()
    
#     if data is None:
#         print("No data to process. Skipping this iteration.")
#         current_iteration += 1
#         time.sleep(60)  # Wait before the next check
#         continue  # Skip to the next iteration

#     # Run GNN
#     output = model(data)
    
#     # Detect anomalies
#     anomalies = detect_anomalies(output)
#     if len(anomalies) > 0:
#         print("Fraud detected:", anomalies)
    
#     # Implement specific fraud detection methods
#     insider_trading_alerts = detect_insider_trading(data)
#     if insider_trading_alerts:
#         print("Insider trading alerts:", insider_trading_alerts)

#     pump_and_dump_alerts = detect_pump_and_dump(data)
#     if pump_and_dump_alerts:
#         print("Pump and dump alerts:", pump_and_dump_alerts)

#     money_laundering_alerts = detect_money_laundering(data)
#     if money_laundering_alerts:
#         print("Money laundering alerts:", money_laundering_alerts)

#     # Analyze transaction descriptions (if applicable)
#     for transaction in data.edge_index.t().tolist():  # Assuming edge_index contains transaction descriptions
#         description = f"Transaction from {transaction[0]} to {transaction[1]}"
#         label, score = analyze_transaction_description(description)
#         print(f"Transaction analysis: {label} with score {score}")

#     current_iteration += 1
#     time.sleep(60)  # Wait before the next iteration


import torch
import torch.nn as nn
import torch.nn.functional as F
from py2neo import Graph
from transformers import pipeline
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

# Define GNN model
class FraudDetectionGNN(nn.Module):
    def __init__(self):
        super(FraudDetectionGNN, self).__init__()
        self.conv1 = GCNConv(32, 16)  # First graph convolution layer
        self.conv2 = GCNConv(16, 8)    # Second graph convolution layer

    def forward(self, data):
        x, edge_index = data.x, data.edge_index  # Unpack data
        x = self.conv1(x, edge_index)  # Apply first convolution
        x = F.relu(x)                  # Apply ReLU activation
        x = self.conv2(x, edge_index)  # Apply second convolution
        return x

# Load GNN model
model_path = "/Users/kanishkaverma/Desktop/fintech-llm/models/falcon_gnn_dgl.pth"  # Update this path if needed
model = FraudDetectionGNN()
model.load_state_dict(torch.load(model_path))
model.eval()

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def fetch_transaction_graph():
    query = """
    MATCH (a:Account)-[t:TRANSACTION]->(b:Account)
    WHERE t.amount > 1000000
    RETURN a, t, b
    """
    result = graph.run(query).data()
    
    # Convert Neo4j result to PyTorch Geometric graph
    edges = []
    for record in result:
        src = int(record['a']['id'])  # Ensure IDs are integers
        dst = int(record['b']['id'])
        edges.append((src, dst))
    
    if not edges:
        print("No edges found in the graph.")
        return None  # Return None or handle the empty case appropriately

    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()  # Create edge index tensor
    x = torch.randn(len(edges), 32)  # Node features (random for example)
    
    # Create a Data object for PyTorch Geometric
    data = Data(x=x, edge_index=edge_index)
    print(f"Edge Index: {edge_index}")
    print(f"Node Features: {x}")
    return data

def detect_anomalies(output, threshold=0.8):
    """
    Detect anomalies based on GNN output.
    """
    anomalies = output[output > threshold]
    return anomalies

# Load LLM for text analysis
fraud_llm = pipeline("text-classification", model="yiyanghkust/finbert-tone")  # Use a suitable model for fraud detection

def analyze_transaction_description(description):
    """
    Analyze transaction description using LLM.
    """
    result = fraud_llm(description)[0]
    return result['label'], result['score']

# Real-time monitoring loop
def monitor_transactions(max_iterations=10):
    current_iteration = 0
    while current_iteration < max_iterations:
        print(f"Iteration {current_iteration + 1} of {max_iterations}")
        
        # Fetch new transactions
        data = fetch_transaction_graph()
        
        if data is not None and data.edge_index.size(1) > 0:  # Check if edge_index is not empty
            # Run GNN
            output = model(data)
            
            # Detect anomalies
            anomalies = detect_anomalies(output)
            if len(anomalies) > 0:
                print("Fraud detected:", anomalies)
        else:
            print("No valid graph data to process.")
        
        current_iteration += 1

if __name__ == "__main__":
    monitor_transactions()