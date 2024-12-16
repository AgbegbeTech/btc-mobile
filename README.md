# BTC-Mobile

BTC-Mobile is an innovative fork of Bitcoin designed to optimize blockchain technology for mobile devices and international communication. By increasing the block size to 2MB and reducing the block time to 2 minutes, BTC-Mobile enhances transaction throughput and reduces confirmation times, making it ideal for modern mobile-first users. Leveraging advanced AI and ML techniques, decentralized storage solutions like IPFS, and over 88 open-source communication protocols, BTC-Mobile aims to bring Satoshi Nakamoto's vision of decentralized peer-to-peer electronic cash to the next generation of users.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development Phases](#development-phases)
- [Contributing](#contributing)
- [License](#license)

## Introduction

BTC-Mobile is designed to address the evolving needs of the Bitcoin community, focusing on mobile optimization, transaction speed, and enhanced security. This project aims to make Bitcoin more accessible and efficient for mobile devices while ensuring secure and decentralized transactions.

## Features

- **Increased Block Size and Reduced Block Time**: Block size increased to 2MB and block time reduced to 2 minutes, enhancing transaction throughput and reducing confirmation times.
- **Simplified Payment Verification (SPV)**: Lightweight nodes for mobile devices to participate in the network without downloading the entire blockchain.
- **IPFS Integration**: Decentralized storage for enhanced data availability and reduced reliance on centralized servers.
- **AI and ML Integration**: Optimizations for various communication protocols, including HTTP/HTTPS, WebSockets, MQTT, CoAP, and many others, ensuring efficient and reliable communication.
- **Support for 88+ Communication Protocols**: Facilitates seamless international transactions and global interoperability.
- **Satellite Communication (SatCom)**: Ensures users in remote and underserved areas can participate in the Bitcoin network.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/btc-mobile.git
    cd btc-mobile
    ```

2. **Install Dependencies**:
    ```bash
    # Example for Python dependencies
    pip install -r requirements.txt
    ```

3. **Set Up the Environment**:
    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```

## Usage

### SPV Client

To start the SPV client:
```python
python spv_client.py
```

### IPFS Integration

To upload data to IPFS:
```python
python ipfs_upload.py "your data here"
```

### PWA

To run the PWA:
```bash
# Serve the PWA using a web server
python -m http.server
```

## Development Phases

### Phase 1: Initial Setup (Months 1-2)
- Fork Bitcoin Core repository and rename the project to BTC-Mobile.
- Set up the development environment and initialize the Git repository.
- Create initial documentation (README.md, LICENSE, CONTRIBUTING.md).

### Phase 2: Core Development (Months 3-6)
- Develop SPV client and integrate IPFS.
- Set up PWA framework and design mobile-friendly UI.
- Adjust blockchain parameters to 2MB block size and 2-minute block time.

### Phase 3: AI and ML Integration (Months 7-9)
- Develop and train AI models for transaction analysis and fraud detection.
- Deploy AI models within the app for real-time analysis and personalized recommendations.

### Phase 4: Data Security and Protocol Integration (Months 10-12)
- Implement data security measures and integrate open-source communication protocols.
- Integrate satellite communication (SatCom) to extend network reach.
- Conduct unit and integration testing, followed by security audits.

### Phase 5: Testing and QA (Months 13-14)
- Perform comprehensive testing and gather user feedback through beta testing.
- Iterate on design and implementation based on feedback.

### Phase 6: Documentation and Community Engagement (Months 15-16)
- Finalize and publish comprehensive documentation.
- Engage with the developer community and prepare for open-source release.

### Phase 7: Deployment and Launch (Months 17-24)
- Prepare for beta launch and conduct beta testing.
- Launch full release and provide ongoing support and updates.

## Contributing

We welcome contributions from the community. Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Sure! Here’s a **README** that summarizes everything we’ve done to set up the SPV node with Flask, Gunicorn, Nginx, and how to integrate it into your **BTC-Mobile project**.

---

# BTC-Mobile Backend Setup - SPV Node with Flask, Gunicorn, and Nginx

This repository sets up a Simplified Payment Verification (SPV) node for interacting with the Bitcoin blockchain via a Flask API. The backend is production-ready using **Gunicorn** as the WSGI server and **Nginx** as a reverse proxy. This setup can be used in mobile applications (BTC-Mobile) to interact with the Bitcoin network, query blockchain data, and verify transactions.

---

## Prerequisites

- **Raspberry Pi 4** (or any similar ARM-based system)
- **Raspberry Pi OS** (preferably 64-bit)
- **Python 3.x** installed
- **Bitcoin Core** (installed in SPV mode)
- **Internet Connection** for downloading dependencies

---

## Setup Instructions

### 1. **Prepare the Raspberry Pi**

First, update your system and install the necessary dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install wget curl git build-essential python3-pip python3-venv nginx -y
```

### 2. **Create a Python Virtual Environment**

We will create and activate a Python virtual environment to isolate the project dependencies.

```bash
python3 -m venv ~/myenv
source ~/myenv/bin/activate
```

Your prompt should now show `(myenv)`.

### 3. **Install Required Python Packages**

Install the necessary Python packages for Flask and Bitcoin RPC:

```bash
pip install flask bitcoinrpc httpx typing_extensions
```

---

### 4. **Install Bitcoin Core (SPV Node)**

Download and install Bitcoin Core, which will run in SPV mode:

```bash
wget https://bitcoincore.org/bin/bitcoin-core-28.0/bitcoin-28.0-aarch64-linux-gnu.tar.gz
tar -xvf bitcoin-28.0-aarch64-linux-gnu.tar.gz
sudo mv bitcoin-28.0/bin/* /usr/local/bin/
```

### 5. **Configure Bitcoin Core**

Create the `bitcoin.conf` file to configure Bitcoin Core to run in SPV mode (lightweight):

```bash
mkdir ~/.bitcoin
nano ~/.bitcoin/bitcoin.conf
```

Add the following configuration:

```conf
server=1
txindex=0
prune=550
blockfilterindex=1
disablewallet=1
rpcuser=bitcoinrpc
rpcpassword=changeme
rpcallowip=127.0.0.1
rpcport=8332
```

### 6. **Start Bitcoin Core in SPV Mode**

Run Bitcoin Core in SPV mode with pruning enabled:

```bash
bitcoind -daemon -reindex
```

---

### 7. **Create Flask API**

Create a Flask API (`spv_api.py`) to interact with the Bitcoin Core node and serve endpoints to fetch blockchain data and verify transactions.

Create the Python file:

```bash
nano spv_api.py
```

Add the following code to `spv_api.py`:

```python
from flask import Flask, jsonify, request
from bitcoinrpc.authproxy import AuthServiceProxy

app = Flask(__name__)

# Replace with your RPC credentials
rpc_user = "bitcoinrpc"
rpc_password = "changeme"
rpc_url = f"http://{rpc_user}:{rpc_password}@127.0.0.1:8332"
rpc_connection = AuthServiceProxy(rpc_url)

@app.route('/headers', methods=['GET'])
def get_headers():
    best_block_hash = rpc_connection.getbestblockhash()
    headers = rpc_connection.getblockheader(best_block_hash)
    return jsonify({"headers": headers})

@app.route('/verify', methods=['POST'])
def verify_transaction():
    txid = request.json.get('txid')
    proof = rpc_connection.gettxoutproof([txid])
    return jsonify({"proof": proof})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

### 8. **Run Flask with Gunicorn**

Gunicorn will serve the Flask app in a production environment.

Install Gunicorn:

```bash
pip install gunicorn
```

Run the Flask app using Gunicorn:

```bash
gunicorn --workers 3 spv_api:app
```

---

### 9. **Set Up Nginx as a Reverse Proxy**

Install Nginx:

```bash
sudo apt install nginx
```

Create a new Nginx configuration for your app:

```bash
sudo nano /etc/nginx/sites-available/spv_api
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name 192.168.2.3;  # Replace with your Raspberry Pi's IP or domain name

    location / {
        proxy_pass http://127.0.0.1:8000;  # Gunicorn will run on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/spv_api /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

### 10. **Set Up Gunicorn as a Systemd Service**

Create a systemd service for Gunicorn to keep it running in the background:

```bash
sudo nano /etc/systemd/system/spv_api.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance to serve spv_api
After=network.target

[Service]
User=pi
Group=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/myenv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 spv_api:app

[Install]
WantedBy=multi-user.target
```

Enable and start the Gunicorn service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable spv_api.service
sudo systemctl start spv_api.service
```

---

### 11. **Test the API**

1. **Test the API locally** using `curl`:
   
   ```bash
   curl http://127.0.0.1:5000/headers
   ```

2. **Test from another device** (e.g., laptop, phone) on the same network using the Raspberry Pi's IP:

   ```bash
   curl http://192.168.2.3:5000/headers
   ```

---

### 12. **Secure the API with SSL (Optional)**

If you'd like to secure the API with HTTPS, you can use **Let’s Encrypt** and **Certbot** for a free SSL certificate:

1. Install Certbot:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. Obtain the SSL certificate:

   ```bash
   sudo certbot --nginx
   ```

---

## **How to Use This Setup for Your BTC-Mobile Project**

1. **Mobile App Integration**:
   Your mobile app can make HTTP requests to the Flask API (running on `http://192.168.2.3:5000`) to query the latest Bitcoin block header, verify transactions, or interact with the Bitcoin network.

2. **Bitcoin Payment Integration**:
   You can use this setup to monitor incoming Bitcoin payments and verify transactions in real-time on your mobile app. For example, a user can make a Bitcoin payment, and your mobile app can use the `/verify` endpoint to check if the transaction is confirmed.

3. **Query Blockchain Data**:
   Your mobile app can use the `/headers` endpoint to fetch the latest blockchain data and display it to users, allowing them to monitor the state of the Bitcoin network.

---

## **Conclusion**

You now have a production-ready environment for interacting with the Bitcoin blockchain using an SPV node, Flask, Gunicorn, and Nginx. This backend is integrated into your **BTC-Mobile project**, allowing your mobile app to communicate with the Bitcoin network and verify transactions efficiently.

