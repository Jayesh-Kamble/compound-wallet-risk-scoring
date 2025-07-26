# fetch_compound_specific.py
# This script fetches all interactions with major Compound V2 contracts for a specific wallet address.
# It uses Alchemy's API (see your .env for the key). This is the "data fetch" step for our risk scoring.

import os
import requests
from dotenv import load_dotenv

# Loads Alchemy API key from the .env file.
load_dotenv()
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
BASE_URL = f'https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}'

# These are the most important Compound contract addresses (protocol controller + the main cTokens).
# We'll use these as filters to make sure we fetch "real" Compound protocol interactions only.
COMPOUND_CONTRACTS = [
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b",  # Comptroller
    "0x39aa39c021dfbae8fac545936693ac917d5e7563",  # cUSDC
    "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5",  # cETH
    "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643",  # cDAI
    "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9"   # cUSDT
]

def fetch_compound_interactions(wallet: str) -> dict:
    """
    Fetches this wallet's history of Compound protocol transactions by calling Alchemy's getAssetTransfers.
    - Only gets transactions involving the main Compound contracts.
    - Returns all kinds of transfer types (ERC20, external, internal).
    
    Args:
        wallet (str): The user wallet address (must be an Ethereum address, 0x...).
    
    Returns:
        dict: {
            "transfers": [ ...list of event dicts... ],
            "total_interactions": int (number of Compound protocol transactions)
        }
    """
    # Prepare the API request to only return interactions with Compound contracts
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "alchemy_getAssetTransfers",
        "params": [{
            "fromAddress": wallet,  # We fetch what this wallet sent to Compound
            "contractAddresses": COMPOUND_CONTRACTS,
            # We want all relevant transaction types that might imply lending/borrowing
            "category": ["erc20", "external", "internal"],
            "withMetadata": True,
            "excludeZeroValue": False,
            "maxCount": "0x64"  # This limits to 100 txs at a time; can raise if needed
        }]
    }
    try:
        # Actually send the request out to Alchemy's Ethereum API
        response = requests.post(BASE_URL, json=payload, timeout=15)
        result = response.json()
        if "error" in result:
            print(f"API Error: {result['error']}")
            return {"transfers": [], "total_interactions": 0}
        # Grab just the actual transfer list back (if non-empty)
        transfers = result.get("result", {}).get("transfers", [])
        return {
            "transfers": transfers,
            "total_interactions": len(transfers)
        }
    except Exception as e:
        print(f"Error while fetching Compound data for wallet {wallet}: {e}")
        return {"transfers": [], "total_interactions": 0}

# That’s it—just pass a wallet to fetch_compound_interactions() to get a summary
# of all their Compound V2 protocol history for risk scoring!
