# compute_features.py
# This script takes in raw Compound protocol transaction data for a wallet
# and transforms it into simple, easy-to-compare numeric features.
# These features (like total transactions, asset diversity, value, etc.)
# are the basis for your wallet risk score model.

import pandas as pd

def compute_features(compound_data: dict) -> pd.Series:
    """
    Given a dictionary of transaction events (from fetch_compound_specific.py),
    this function computes a set of risk features for a single wallet.
    Main features:
      - tx_count: How many Compound protocol transactions did this wallet do?
      - avg_value: What was the average value of those Compound txs?
      - unique_assets: How many different Compound assets (e.g. cTokens) were touched?
      - activity_score: Simple "summary" metric, capped so it doesn't go wild with super-active wallets.
    """
    # Grab the list of transfers from previous fetch
    transfers = compound_data.get("transfers", [])
    
    # If the wallet had no Compound transactions, set everything to zero.
    if not transfers:
        return pd.Series({
            "tx_count": 0,
            "avg_value": 0,
            "unique_assets": 0,
            "activity_score": 0
        })

    # Turn the list of transfers into a Pandas DataFrame for quick math
    df = pd.DataFrame(transfers)
    
    # Just count the number of rows to get total Compound protocol txs
    tx_count = len(df)

    # Take the mean value of all transactions (if present), 0 otherwise
    avg_value = df.get('value', pd.Series([0])).astype(float).mean() if 'value' in df else 0

    # Count how many unique assets (e.g. different cTokens) this wallet touched
    unique_assets = df.get('asset', pd.Series()).nunique() if 'asset' in df else 0

    # Make a simple "activity score" (here: tx_count times 10, but max 100)
    activity_score = min(tx_count * 10, 100)

    # Return all these as a row/Series; keys here match the input to your scoring function
    return pd.Series({
        "tx_count": tx_count,
        "avg_value": avg_value,
        "unique_assets": unique_assets,
        "activity_score": activity_score
    })

# This way, anyone reading your code will quickly understand what features you use, why,
# and how they'll get used in scoring risk for each wallet!
