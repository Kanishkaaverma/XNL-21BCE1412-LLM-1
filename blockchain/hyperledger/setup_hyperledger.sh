# Install Hyperledger Fabric
curl -sSL https://bit.ly/2ysbOFE | bash -s -- 2.2.3 1.5.1

# Start the network
cd fabric-samples/test-network
./network.sh up createChannel -c mychannel