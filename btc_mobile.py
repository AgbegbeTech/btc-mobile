import hashlib
import time
import json
import grpc
import ipfshttpclient
import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.ipfs_client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.create_block(data="Genesis Block", previous_hash="0")
        self.chain.append(genesis_block)

    def create_block(self, data, previous_hash):
        index = len(self.chain)
        timestamp = int(time.time())
        hash = self.calculate_hash(index, previous_hash, timestamp, data)
        block = Block(index, previous_hash, timestamp, data, hash)
        block_ipfs_hash = self.store_block_on_ipfs(block)
        block.data = block_ipfs_hash  # Store IPFS hash instead of raw data
        return block

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = f"{index}{previous_hash}{timestamp}{data}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def store_block_on_ipfs(self, block):
        block_data = json.dumps(block.__dict__)
        res = self.ipfs_client.add_bytes(block_data.encode('utf-8'))
        return res

    def retrieve_block_from_ipfs(self, ipfs_hash):
        block_data = self.ipfs_client.cat(ipfs_hash)
        block_dict = json.loads(block_data)
        return Block(**block_dict)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        if self.is_valid_new_block(new_block, self.get_latest_block()):
            self.chain.append(new_block)

    def is_valid_new_block(self, new_block, previous_block):
        if previous_block.index + 1 != new_block.index:
            return False
        if previous_block.hash != new_block.previous_hash:
            return False
        if self.calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data) != new_block.hash:
            return False
        return True

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class CoinbaseTransaction(Transaction):
    def __init__(self, recipient, amount):
        super().__init__(sender="coinbase", recipient=recipient, amount=amount)

# Lightning Network Integration
class LightningNetwork:
    def __init__(self, node_url, cert_path, macaroon_path):
        self.node_url = node_url
        self.cert_path = cert_path
        self.macaroon_path = macaroon_path
        self.channel = self.connect_to_lnd()
        self.stub = lnrpc.LightningStub(self.channel)

    def connect_to_lnd(self):
        with open(self.cert_path, 'rb') as f:
            cert = f.read()
        creds = grpc.ssl_channel_credentials(cert)
        with open(self.macaroon_path, 'rb') as f:
            macaroon = f.read()
        auth_creds = grpc.metadata_call_credentials(lambda context, callback: callback([('macaroon', macaroon.hex())], None))
        combined_creds = grpc.composite_channel_credentials(creds, auth_creds)
        return grpc.secure_channel(self.node_url, combined_creds)

    def create_invoice(self, amount, memo):
        request = ln.Invoice(value=amount, memo=memo)
        response = self.stub.AddInvoice(request)
        return response.payment_request

    def pay_invoice(self, payment_request):
        request = ln.SendRequest(payment_request=payment_request)
        response = self.stub.SendPaymentSync(request)
        return response.payment_preimage

# Example usage of Lightning Network
node_url = 'localhost:10009'
cert_path = '/path/to/tls.cert'
macaroon_path = '/path/to/admin.macaroon'
ln = LightningNetwork(node_url, cert_path, macaroon_path)

class BTCMobileBlockchain(Blockchain):
    def __init__(self, block_size, difficulty):
        self.block_size = block_size
        self.difficulty = difficulty
        super().__init__()

    def create_genesis_block(self):
        genesis_data = {
            "transactions": [CoinbaseTransaction(recipient="first_miner", amount=50).__dict__],
            "block_size": self.block_size,
            "difficulty": self.difficulty
        }
        genesis_block = self.create_block(data=json.dumps(genesis_data), previous_hash="0")
        self.chain.append(genesis_block)

# Initialize BTC-Mobile blockchain with optimized parameters
btc_mobile_chain = BTCMobileBlockchain(block_size=2 * 1024 * 1024, difficulty=2 * 60)  # 2MB block size, 2-minute block time

# Example of adding a new block
new_block_data = {
    "transactions": [Transaction(sender="user1", recipient="user2", amount=10).__dict__],
    "block_size": btc_mobile_chain.block_size,
    "difficulty": btc_mobile_chain.difficulty
}
previous_block = btc_mobile_chain.get_latest_block()
new_block = btc_mobile_chain.create_block(data=json.dumps(new_block_data), previous_hash=previous_block.hash)
btc_mobile_chain.add_block(new_block)

# Print the blockchain
for block in btc_mobile_chain.chain:
    print(vars(block))