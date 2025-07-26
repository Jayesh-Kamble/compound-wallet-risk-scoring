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

- Alchemy `getAssetTransfers` endpoint is used to retrieve ERC20/external/internal transactions involving Compound V2 controller and main cTokens.

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

<img width="549" height="460" alt="image" src="https://github.com/user-attachments/assets/6541ea14-075e-4180-9d30-dc462fc10cb5" />

---

## 📊 Visualizations

Below are some visual insights from the computed wallet risk scores:

### 🔹 1. Distribution of Wallet Risk Scores

Shows how risk scores are distributed across wallets most wallets are low-risk, with a few outliers.

<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/2b75a2a0-56a6-4359-b2d0-47d89479ed8d" />


---

### 🔹 2. Boxplot of Wallet Risk Scores

Highlights the presence of outliers and the spread of risk scores in a single visual.

<img width="790" height="390" alt="image" src="https://github.com/user-attachments/assets/7916621e-ed3f-4bbe-8c9d-876b8f720f54" />


---

### 🔹 3. Top 5 and Bottom 5 Wallet Risk Scores

Compares the riskiest and least risky wallets based on their score. A helpful visual to identify extremes.

<img width="1181" height="590" alt="image" src="https://github.com/user-attachments/assets/4f08d5af-f284-48ca-a3be-1b936e82acfb" />


---

## 📈 Improvements / Future Work

- Separate supply, borrow, and redeem events for deeper risk profiling  
- Add health factor/liquidation signals from richer subgraph data  
- Incorporate time-weighted recency (recent actions more relevant)  
- Compare scores to actual risk events or performance  
- Add visualizations (e.g., distribution of scores, asset heatmap)

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
│   ├── wallets.txt
│   ├── 1.png
│   ├── 2.png
│   └── 3.png
└── wallet_risk_scores.csv
```

---

## 🙋‍♂️ About

Hi, I’m Jayesh Kamble!  
This repo is my solution for Zeru AI’s DeFi wallet risk scoring challenge.  
Questions, feedback, or just want to chat about DeFi? Reach out anytime!

---

## 📧 Contact

- [LinkedIn](https://www.linkedin.com/in/jayesh-kamble-/)
- [GitHub](https://github.com/Jayesh-Kamble/)

> Analyzing wallet risk is essential for safe, scalable DeFi. Thanks for reviewing!
