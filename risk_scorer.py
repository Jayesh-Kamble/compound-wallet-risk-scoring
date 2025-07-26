# risk_scorer.py
# This module takes the numeric features extracted from a wallet's Compound protocol activity
# and turns them into a single risk score (from 0 to 1000).
# More activity and value = higher score, inactive = low score.

import pandas as pd

class RiskScorer:
    # This function takes a Series of features (from compute_features.py)
    # and calculates a risk score for that wallet.
    def score_wallet(self, features: pd.Series) -> int:
        # How many Compound protocol transactions did the wallet do?
        tx_count = features.get('tx_count', 0)
        # What was the average value of those transactions?
        avg_value = features.get('avg_value', 0)
        # How many different cTokens/assets did the wallet use?
        unique_assets = features.get('unique_assets', 0)
        # Activity summary: a simple, capped score.
        activity_score = features.get('activity_score', 0)
        
        # If there were no Compound transactions, assign a low default risk.
        if tx_count == 0:
            return 100  # Low risk, since the wallet didn't use Compound
        
        # Otherwise, calculate risk as a weighted sum of the features.
        # More activity, value, diversity, and overall action means higher risk.
        risk_score = (
            tx_count * 20 +                       # Frequent use raises risk
            min(avg_value / 1000, 50) +           # Big tx values contribute, but capped
            unique_assets * 10 +                  # Using more assets bumps risk up
            activity_score * 2                    # Higher capped activity = higher risk
        )
        
        # Score is always kept between 0 and 1000
        return min(max(int(risk_score), 0), 1000)

# Usage example for this class:
# from compute_features import compute_features
# features = compute_features(compound_data)
# scorer = RiskScorer()
# score = scorer.score_wallet(features)
