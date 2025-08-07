import time
import requests
from uniswap_router import swap_token
from config import CREATOR_ADDRESS, MIN_ETH_TO_SPEND

ZORA_API_URL = ""  # WHERE IS THE ZORA API LINK?

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def get_latest_post():
    query = {
        "query": """
        query LatestToken($address: String!) {
            tokens(
                where: {creatorAddresses: [$address]}
                sort: { sortKey: MINTED_TIMESTAMP, sortDirection: DESC }
                pagination: { limit: 1 }
            ) {
                nodes {
                    token {
                        tokenId
                        collectionAddress
                        mintInfo {
                            price {
                                eth
                            }
                        }
                    }
                }
            }
        }
        """,
        "variables": {
            "address": CREATOR_ADDRESS
        }
    }

    try:
        response = requests.post(ZORA_API_URL, json=query, headers=HEADERS)
        result = response.json()
        token_data = result["data"]["tokens"]["nodes"][0]["token"]
        token_address = token_data["collectionAddress"]
        token_id = token_data["tokenId"]
        mint_price = float(token_data["mintInfo"]["price"]["eth"])
        return token_address, token_id, mint_price
    except Exception as e:
        print(f"[!] Error getting latest post: {e}")
        return None, None, None


def monitor_loop():
    seen_posts = set()

    while True:
        token_address, token_id, mint_price = get_latest_post()

        if token_address and token_id:
            unique_key = f"{token_address}-{token_id}"
            if unique_key not in seen_posts:
                print(
                    f"[+] New token detected: {token_address}, Token ID: {token_id}, Mint price: {mint_price} ETH")

                # Langsung beli tanpa pengecekan harga
                print("[*] Initiating token swap as early buyer...")
                swap_token(token_address, MIN_ETH_TO_SPEND)

                seen_posts.add(unique_key)

        time.sleep(8)  # cek tiap 8 detik


if __name__ == "__main__":
    monitor_loop()
