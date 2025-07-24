### Repository: GhostBalance
# Description: A stealthy tool that checks for dormant wallet balances across multiple chains to discover "forgotten" funds.

# Structure:
# ghostbalance/
# ├── main.py
# ├── chains.py
# ├── wallet_scanner.py
# ├── requirements.txt
# └── README.md

# --- chains.py ---
SUPPORTED_CHAINS = {
    "ethereum": {
        "rpc": "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
        "explorer": "https://etherscan.io/address/"
    },
    "polygon": {
        "rpc": "https://polygon-rpc.com",
        "explorer": "https://polygonscan.com/address/"
    },
    "bsc": {
        "rpc": "https://bsc-dataseed.binance.org/",
        "explorer": "https://bscscan.com/address/"
    }
}

# --- wallet_scanner.py ---
import random
import time
from web3 import Web3

def check_balance(rpc_url, address):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.isConnected():
        return None
    try:
        balance = w3.eth.get_balance(address)
        return w3.fromWei(balance, 'ether')
    except Exception:
        return None

def is_dormant(w3, address, days_threshold=180):
    try:
        txs = w3.eth.get_block('latest')['number']
        history = w3.eth.get_transaction_count(address)
        return history == 0
    except:
        return False

def random_wallet():
    """Generates a random-looking wallet address."""
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

# --- main.py --import time
from chains import SUPPORTED_CHAINS
from wallet_scanner import check_balance, random_wallet

if __name__ == "__main__":
    print("🔍 Scanning for ghost wallets... (Ctrl+C to stop)")
    try:
        while True:
            wallet = random_wallet()
            for chain, data in SUPPORTED_CHAINS.items():
                balance = check_balance(data['rpc'], wallet)
                if balance and balance > 0.01:
                    print(f"💰 Found {balance:.4f} on {chain.upper()} - {data['explorer']}{wallet}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Scan stopped.")




