# main.py
# Author: Jayesh Kamble
# Description:
# This script calculates a risk score for each wallet in the Compound protocol dataset.
# It fetches Compound transaction data for each address, computes simple risk features,
# and outputs a CSV with wallet IDs and scores.

import pandas as pd
from fetch_compound_specific import fetch_compound_interactions
from compute_features import compute_features
from risk_scorer import RiskScorer

def main():
    # Try to read the wallet list (should be 1 address per line)
    try:
        with open("data/wallets.txt", "r") as f:
            # Clean up wallet addresses (no whitespace, all lowercase)
            wallets = [line.strip().lower() for line in f if line.strip()]
    except Exception as err:
        print("Could not read wallets.txt - check if the file exists?")
        return
    
    # Instantiate my scoring class (see risk_scorer.py)
    scorer = RiskScorer()
    results = []

    # Loop through every wallet address
    for i, wallet in enumerate(wallets):
        print(f"[{i+1}/{len(wallets)}] Processing: {wallet}")
        
        # Step 1: Fetch Compound protocol-related activity for the wallet
        compound_data = fetch_compound_interactions(wallet)
        
        # Step 2: Turn raw data into meaningful risk features (see compute_features.py)
        features = compute_features(compound_data)
        
        # Step 3: Convert those features into a risk score (range: 0-1000)
        risk_score = scorer.score_wallet(features)
        
        # Store for output
        results.append({'wallet_id': wallet, 'score': risk_score})

    # Make a DataFrame so I can easily save as CSV
    df = pd.DataFrame(results)
    df.to_csv('wallet_risk_scores.csv', index=False)
    print("Saved wallet scores to wallet_risk_scores.csv - all done!")

if __name__ == "__main__":
    main()
