from hfc.fabric import Client

def log_transaction(transaction):
    c = Client(net_profile="test/fixtures/network.json")
    c.new_channel('mychannel')
    response = c.chaincode_invoke(
        requestor='Admin',
        channel_name='mychannel',
        peers=['peer0.org1.example.com'],
        args=[transaction],
        cc_name='mycc',
        fcn='invoke'
    )
    return response

# Example usage
if __name__ == "__main__":
    transaction = {"amount": 1000, "description": "Stock purchase"}
    response = log_transaction(transaction)
    print(f"Transaction Logged: {response}")