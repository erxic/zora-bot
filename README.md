# Zora Trading Bot

Bot ini memonitor kreator Zora dan secara otomatis membeli token baru

## Fitur

- Monitoring postingan kreator Zora.
- Deteksi token terbaru secara real-time.
- Eksekusi pembelian token otomatis via Uniswap V4.

## Konfigurasi

Buat file `.env` seperti berikut:

```env
PRIVATE_KEY=your_private_key_here
WALLET_ADDRESS=your_wallet_address
RPC_URL=https://zora-mainnet.g.alchemy.com/v2/your_project_id
UNIVERSAL_ROUTER_ADDRESS=
CREATOR_ADDRESS=
MIN_ETH_TO_SPEND=0.0001
```
