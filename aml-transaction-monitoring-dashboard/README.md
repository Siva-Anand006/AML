# AML Transaction Monitoring & Suspicious Activity Dashboard

An interactive, high-fidelity Streamlit transaction monitoring dashboard that simulates an end-to-end anti-money laundering (AML) compliance workflow. It applies custom rule-based detection typologies, computes weighted transaction risk scores, establishes priority alert tiers, and auto-generates compliance narrative summaries using synthetic data modeled after the Kaggle **SAML-D** dataset schema.

---

## 🎯 Business Context & Problem Statement
Financial institutions are legally obligated under Banking Secrecy Act (BSA) and USA PATRIOT Act regulations to establish robust Transaction Monitoring Systems (TMS) to detect, prevent, and report suspicious activities. Manual audit processes are expensive, lag behind real-time velocity, and are highly prone to alert fatigue. 

This dashboard serves as a mock Compliance Decision Engine Cockpit. It automates:
1. **Rule flagging** across high-probability indicators (e.g., structuring, rapid frequency).
2. **Weighted risk scoring** (0-100) to classify transactions into actionable priority tiers (Low, Medium, High, Critical).
3. **Structured narrative generation** to eliminate compliance officer report-writing bottlenecks for Suspicious Activity Reports (SAR).

---

## 📊 Dataset Schema & Synthetic Generator
This project includes a high-fidelity synthetic generator (`src/synthetic_generator.py`) modeled after the Kaggle **SAML-D (Synthetic Anti-Money Laundering Dataset)** schema. It automatically populates the `data/aml_transactions.csv` file with transactions featuring:
*   `Time` / `Date`: Simulated chronological sequences.
*   `Sender_account` / `Receiver_account`: Consistent account tags.
*   `Amount`: Lognormal baseline transaction distribution with injected spikes.
*   `Payment_currency` / `Received_currency`: Multi-currency support.
*   `Sender_bank_location` / `Receiver_bank_location`: Geographic indicators mapping normal countries vs high-risk jurisdictions.
*   `Payment_type`: ACH, Wire, Credit Card, Debit Card, Cheque, and Cash Transfer.
*   `Is_laundering`: Underlying ground truth flag.

### Injected Money Laundering Typologies:
*   **Structuring (Smurfing):** Senders placing multiple rapid transfers between $9,000 and $9,990 to bypass the legal currency transaction reporting (CTR) threshold of $10,000.
*   **High Velocity:** Senders executing 12-20 transactions in rapid succession within a single day.
*   **High-Risk Geographies:** Direct transaction exposure involving blacklisted or high-risk jurisdictions (Iran, North Korea, Syria, Russia, Myanmar, Afghanistan).
*   **Unusual Amount Spikes:** Account holders executing transfers exceeding 3x-8x their historical average transaction value.
*   **Massive High-Value Whales:** Extreme volume transfers ($150,000 - $450,000) representing high-risk wealth movements.

---

## ⚙️ AML Detection Rules Engine & Weighted Risk Model

### 1. Detection Rules:
*   **High Value (`rule_high_value`):** Exceeds the 99th percentile of all global transactions.
*   **Unusual Amount (`rule_unusual_amount`):** Transaction amount is > 3x the sender's average transaction amount (requires > 1 historical txns).
*   **High Velocity (`rule_high_velocity`):** Number of transactions sent is >= 95th percentile of transaction frequencies.
*   **Structuring (`rule_structuring`):** Transaction amount falls between $9,000 and $9,999.99.
*   **High Total Value (`rule_high_total_sender_value`):** Total historical volume of sender is >= 95th percentile.
*   **High-Risk Country (`rule_high_risk_country`):** Sender or receiver bank is located in a high-risk geography.

### 2. Weighted Risk Score Model:
The `src/risk_scoring.py` engine computes a composite risk score (0-100) using custom regulatory risk weights:

| Rule Violation | Weight (Points) | Regulatory Rationale |
| :--- | :---: | :--- |
| **High-Risk Country Link** | `30` | Direct association with sanctions or high-risk jurisdictions. |
| **Structuring / Smurfing** | `25` | Deliberate avoidance of federal CTR reporting thresholds. |
| **High-Value Outlier** | `25` | High financial exposure representing high-impact transfers. |
| **Unusual Amount Spike** | `20` | Significant deviation from customer's historical profile. |
| **High transaction velocity** | `20` | Rapid dispersal of funds indicative of layering stages. |
| **High Total Sender Value** | `15` | Elevated overall account volume over a short time. |

*   **Risk Tiers:** Low (`0-24`), Medium (`25-49`), High (`50-74`), Critical (`75-100`).
*   **Alert Generation:** Transactions with a score `🏆 >= 50` (High/Critical) automatically enter the Suspicious Alert Queue.

---

## 🚀 Key Dashboard Features
1.  **Executive KPIs:** High-visibility cockpit showing total processed transactions, active alerts, alert rates, total suspicious volume, and flagged accounts.
2.  **Interactive Filtering Panel:** Real-time sidebar controls to filter the view by risk level, transaction type, and transaction amounts.
3.  **Advanced Plotly Visualizations:** 
    *   *Transaction Volume by Risk Tier*: Vertical bar chart using color-coded metrics.
    *   *Transaction Value by Transfer Method*: Donut chart illustrating which mechanisms represent the highest volume.
    *   *Rule Violation Frequency*: Horizontal bar chart highlighting which typologies are most commonly violated.
4.  **Suspicious Alert Queue Table:** Searchable grid featuring sorting and progress-bar risk score visualizers, with integrated CSV exporting.
5.  **SAR Narrative Generator:** Dropdown selectors that generate complete, copy-paste-ready suspicious activity reports.

---

## 🛠️ How to Run Locally

### 1. Clone & Set Up Directory
Navigate to the directory:
```bash
cd aml-transaction-monitoring-dashboard
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Dashboard
```bash
streamlit run app.py
```

---

## 📝 Resume Bullet Point
**AML Transaction Monitoring Dashboard | Python, Pandas, Streamlit, SQL Logic**
*   Built a Streamlit-based AML transaction monitoring cockpit using synthetic data modeled after Kaggle's SAML-D dataset to audit suspicious financial activity and generate compliance case narratives.
*   Developed a rule-based transaction evaluation engine and weighted risk scoring model (0-100) using Pandas vectorized operations to classify transfers into Low, Medium, High, and Critical risk tiers.
*   Created interactive data filtering grids, customized Plotly visualizations, a CSV alert downloader, and an auto-generated narrative compliance report generator, significantly reducing compliance review bottlenecks.
