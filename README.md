# 🏦 Compound Wallet Risk Scoring

Analyze DeFi wallet risk using on-chain Compound protocol data.

This project calculates a simple, data-driven risk score for 100+ Ethereum wallets based on their lending/borrowing activity on Compound V2, as part of the Zeru AI internship assignment.

---

## 🚩 Problem Statement

**Goal:**  
- Fetch Compound protocol transaction history for a list of wallets  
- Compute features reflecting each wallet’s risk profile  
- Assign a 0–1000 risk score per wallet based on DeFi protocol activity  

---

## 🛠️ Solution Overview

- **Data fetching:** Uses [Alchemy API](https://docs.alchemy.com/reference/alchemy-getassettransfers) to pull transactions involving major Compound contracts  
- **Feature extraction:** Calculates each wallet’s:  
    - Compound transaction count  
    - Average transaction value  
    - Number of unique Compound assets used  
    - Activity-based score  
- **Flexible scoring function:** Higher activity, more value, and greater asset diversity yield higher risk (0 = lowest, 1000 = highest risk)  

---

## 🚀 Quickstart

1. **Clone this repo:**

    ```bash
    git clone https://github.com/Jayesh-Kamble/compound-wallet-risk-scoring.git
    cd compound-wallet-risk-scoring
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Add your Alchemy API key:**

    - Copy `.env.example` to `.env`  
    - Paste:  
      ```
      ALCHEMY_API_KEY=your-key-here
      ```

4. **Provide wallets:**  
    - List Ethereum addresses (one per line) in `data/wallets.txt`

5. **Run the pipeline:**

    ```bash
    python main.py
    ```

6. **Results:**  
    - `wallet_risk_scores.csv` will contain your scored wallets!

---

## 💡 How It Works

### Data Collection

- Alchemy `getAssetTransfers` endpoint is used to retrieve ERC20/external/internal txs involving Compound V2 controller and main cTokens.

### Feature Selection

| Feature        | Rationale                                         |
|----------------|---------------------------------------------------|
| tx_count       | More Compound txs = more protocol exposure        |
| avg_value      | Higher average = more capital at risk             |
| unique_assets  | More markets/assets may mean diversified risk     |
| activity_score | Simple summary (capped, for stability)            |

### Scoring Method

Risk score (range 0–1000) is calculated as:

```
risk_score = (
    tx_count * 20 +
    min(avg_value / 1000, 50) +
    unique_assets * 10 +
    activity_score * 2
)
```

Clipped to max 1000.  
Inactive wallets default to a low score.

---

## 📝 Example Output

| wallet_id                                  | score |
|-------------------------------------------|-------|
| 0xfaa0768bde629806739c3a4620656c5d26f44ef2 | 732   |
| 0x13b1c8b0e696aff8b4fee742119b549b605f3cbc | 230   |
| ...                                       | ...   |

---

## 📈 Improvements/Future Work

- Separate supply, borrow, and redeem events for deeper risk profiling  
- Add health factor/liquidation signals from richer subgraph data  
- Incorporate time-weighted recency (recent actions more relevant)  
- Compare scores to actual risk events or performance  

---

## 📂 Project Structure

```
compound-wallet-risk-scoring/
├── main.py
├── fetch_compound_specific.py
├── compute_features.py
├── risk_scorer.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── data/
│   └── wallets.txt
└── wallet_risk_scores.csv

```

---
🙋‍♂️ About
Hi, I’m Jayesh Kamble!
This repo is my solution for Zeru AI’s DeFi wallet risk scoring challenge.
Questions, feedback, or just want to chat about DeFi? Reach out anytime!

---

## 📧 Contact
- [LinkedIn]((https://www.linkedin.com/in/jayesh-kamble-/)) 

> Analyzing wallet risk is essential for safe, scalable DeFi. Thanks for reviewing!
