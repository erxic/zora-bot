import json
from web3 import Web3
from config import (
    RPC_URL,
    PRIVATE_KEY,
    WALLET_ADDRESS,
    ROUTER_ADDRESS,
    WETH_ADDRESS,
)

# Inisialisasi Web3 dan akun
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Load ABI Universal Router V4
with open("universal_router_abi.json") as f:
    ROUTER_ABI = json.load(f)

# Inisialisasi contract router
router_contract = w3.eth.contract(
    address=Web3.to_checksum_address(ROUTER_ADDRESS), abi=ROUTER_ABI
)


def swap_token(token_out_address: str, eth_amount: float):
    """
    Fungsi untuk men-swap ETH menjadi token menggunakan Universal Router V4.
    :param token_out_address: Alamat kontrak token tujuan (ERC-20).
    :param eth_amount: Jumlah ETH yang ingin dibelikan token.
    """
    try:
        # Konversi alamat dan nilai
        token_out_address = Web3.to_checksum_address(token_out_address)
        eth_amount_wei = w3.to_wei(eth_amount, "ether")

        print(f"[+] Swapping {eth_amount} ETH for token: {token_out_address}")

        # Nilai minimal token yang diharapkan diterima (anti-slippage)
        min_amount_out = 1

        # Komando untuk V3_SWAP_EXACT_IN di Universal Router: 0x00 (contoh)
        commands = b"\x00"

        # Format data V3SwapExactIn (tokenIn, tokenOut, minAmountOut, recipient)
        encoded_input = (
            WETH_ADDRESS[2:].rjust(64, "0") +
            token_out_address[2:].rjust(64, "0") +
            hex(min_amount_out)[2:].rjust(64, "0") +
            WALLET_ADDRESS[2:].rjust(64, "0")
        )

        inputs = [bytes.fromhex(encoded_input)]

        # Build transaksi ke Universal Router
        tx = router_contract.functions.execute(
            commands,
            inputs,
            # deadline 5 menit
            int(w3.eth.get_block('latest')['timestamp']) + 300
        ).build_transaction({
            "from": WALLET_ADDRESS,
            "value": eth_amount_wei,
            "nonce": w3.eth.get_transaction_count(WALLET_ADDRESS),
            "gas": 800_000,
            "gasPrice": w3.eth.gas_price,
        })

        # Sign dan kirim transaksi
        signed_tx = w3.eth.account.sign_transaction(
            tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[✓] Swap transaction sent: {w3.to_hex(tx_hash)}")

    except Exception as e:
        print(f"[!] Swap failed: {e}")
