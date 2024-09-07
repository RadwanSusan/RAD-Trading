# src\RAD_trading\blockchain\blockchain_data.py
import requests
import pandas as pd
class BlockchainDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.blockchair.com"
    def get_bitcoin_data(self, endpoint, params=None):
        url = f"{self.base_url}/bitcoin/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    def get_latest_blocks(self, limit=10):
        data = self.get_bitcoin_data("blocks", {"limit": limit})
        return pd.DataFrame(data['data'])
    def get_transaction_data(self, tx_hash):
        data = self.get_bitcoin_data(f"dashboards/transaction/{tx_hash}")
        return data['data'][tx_hash]
    def get_address_data(self, address):
        data = self.get_bitcoin_data(f"dashboards/address/{address}")
        return data['data'][address]
    def get_mempool_data(self):
        data = self.get_bitcoin_data("mempool")
        return pd.DataFrame(data['data'])
