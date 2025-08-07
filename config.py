import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
ROUTER_ADDRESS = os.getenv("ROUTER_ADDRESS")
WETH_ADDRESS = os.getenv("WETH_ADDRESS")
MIN_ETH_TO_SPEND = float(os.getenv("MIN_ETH_TO_SPEND", "0.0001"))
CREATOR_ADDRESS = "0x178328430b021261bfe3156436c1ae77bb353c45"  # akun target
