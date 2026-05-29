# AML Transaction Monitoring & Alerting Dashboard

A lightweight, local Streamlit dashboard designed to simulate anti-money laundering (AML) detection workflows, weighted risk scoring, and Suspicious Activity Report (SAR) narrative generation. The application uses a synthetic transaction generator modeled after the Kaggle **SAML-D** dataset schema to simulate realistic financial activity and common money laundering typologies.

## Overview

Compliance teams at financial institutions use Transaction Monitoring Systems (TMS) to spot potential money laundering, structuring, and other suspicious activities. 

This dashboard serves as a functional mock-up of a Compliance Decision Engine, demonstrating:
1. **Rule-Based Flagging**: Captures typical red flags (e.g., rapid velocity, structuring/smurfing, exposure to sanctioned countries).
2. **Weighted Risk Scoring**: Computes a composite score (0-100) to classify transactions into Low, Medium, High, and Critical risk tiers.
3. **SAR Narrative Generation**: Auto-generates structured narratives to help compliance officers draft Suspicious Activity Reports (SAR) more quickly.

## Project Structure

```
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── data/
│   └── aml_transactions.csv   # Synthetic transaction dataset
└── src/
    ├── __init__.py
    ├── data_loader.py         # File reader & state manager
    ├── synthetic_generator.py # Generator for Kaggle SAML-D style data
    ├── rules_engine.py        # Boolean flags for regulatory rules
    ├── risk_scoring.py        # Core weighted scoring logic
    └── case_report.py         # Text builder for SAR narrative reports
```

## Detection Typologies & Scoring Model

### 1. Injected Typologies
The synthetic generator (`src/synthetic_generator.py`) injects realistic money laundering patterns into the dataset:
*   **Structuring (Smurfing)**: Multiple rapid transactions placed just below the $10,000 Currency Transaction Report (CTR) filing threshold (typically between $9,000 and $9,990).
*   **High Velocity**: Rapid layering schemes where an account executes a high frequency of transfers within a single day.
*   **High-Risk Geographies**: Exposure to sanctioned or high-risk jurisdictions.
*   **Unusual Spikes**: Spontaneous transfers that deviate significantly (3x-8x) from the sender's baseline behavior.

### 2. Risk Scoring Engine
The rules engine in `src/rules_engine.py` checks each transaction against several indicators. The scoring engine (`src/risk_scoring.py`) then computes a composite risk score (0-100) using custom weights:

| Rule Violation | Weight | Compliance Rationale |
| :--- | :---: | :--- |
| **High-Risk Country Link** | `30` | Direct association with sanctioned or high-risk regions. |
| **Structuring / Smurfing** | `25` | Evasion of federal CTR reporting thresholds. |
| **High-Value Outlier** | `25` | Significant volume representing elevated financial exposure. |
| **Unusual Amount Spike** | `20` | Outlier compared to historical customer behavior. |
| **High Transaction Velocity** | `20` | Rapid dispersal of funds indicative of layering stages. |
| **High Total Sender Value** | `15` | Elevated overall account volume over a short time frame. |

*   **Risk Tiers**: Low (`0-24`), Medium (`25-49`), High (`50-74`), Critical (`75-100`).
*   **Alert Threshold**: Any transaction with a score of `50` or higher is flagged and sent to the compliance queue.

## Features

*   **KPI Scorecard**: Summarizes key metrics (total transactions, active alerts, suspicious volume, alert rate, flagged accounts).
*   **Interactive Sidebar Filters**: Filter transactions by risk level, payment method, and amount thresholds.
*   **Data Visualizations**: Built-in Plotly charts showing transaction risk distribution, payment type breakdown, and rule violation frequencies.
*   **Staged Alert Queue**: Searchable and sortable data table for compliance analysis, with an export-to-CSV utility.
*   **SAR Narrative Assistant**: Allows analysts to select a flagged transaction and instantly generate a standardized narrative summarizing the activity, actors, and regulatory reasons for filing.

## Getting Started

### Prerequisites
*   Python 3.8 or higher

### Installation & Run
1. Clone the repository and navigate to the directory:
   ```bash
   cd aml-transaction-monitoring-dashboard
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
