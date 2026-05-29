# ISO 27001 GRC & Internal Audit Dashboard

A local, Streamlit-based Governance, Risk, and Compliance (GRC) dashboard built to simulate information security compliance tracking, enterprise risk registries, internal audits, and vendor security assessments. It dynamically computes compliance index metrics, visualizes risk matrices, and generates executive-ready markdown reports.

## Overview

Organizations maintaining or prepping for ISO/IEC 27001:2022 need a way to track the health of their controls, document audit findings, register risks, and log remediation activities. Using disconnected spreadsheets often leads to data duplication and lack of department-level clarity.

This tool consolidates those datasets into a single dashboard, showing:
1. **Control Auditing**: Track status (Compliant, Partially Compliant, Non-Compliant) and review schedules for 20 sample Annex A controls.
2. **Enterprise Risk Register**: Likelihood-impact (5x5) risk matrix mapping to organizational departments.
3. **Audit & Remediation Tracking**: Links internal audit findings to specific failed controls, mapping out action items and due dates.
4. **Third-Party Vendor Management**: Track vendor contract periods, sensitivity, and assessment ratings.
5. **Executive Summary Generator**: Pulls active data states into a structured markdown advisory memo for leadership review.

## File Structure

```
├── app.py                      # Streamlit UI & interactive dashboards
├── requirements.txt            # Package dependencies
├── README.md                   # Setup guide and technical overview
├── data/                       # CSV databases
│   ├── controls.csv
│   ├── risks.csv
│   ├── audit_findings.csv
│   ├── remediation.csv
│   └── vendors.csv
└── src/                        # Core Python scripts
    ├── __init__.py
    ├── data_generator.py       # Coherent synthetic data builder
    ├── data_loader.py          # Session-state loader & CSV write-backs
    ├── risk_scoring.py         # Risk level logic & matrix builders
    ├── compliance_metrics.py   # Aggregation KPIs & compliance formula
    └── report_generator.py     # Executive report compiler
```

## Logic & Calculations

### 1. ISO 27001 Compliance Index
Calculates a weighted compliance percentage based on control status:
$$\text{Compliance Score (\%)} = \frac{\text{Compliant Controls} + (0.5 \times \text{Partially Compliant Controls})}{\text{Total Controls}} \times 100$$

### 2. Risk Matrix Math
Calculates risk scores following typical qualitative frameworks:
$$\text{Risk Score} = \text{Likelihood (1-5)} \times \text{Impact (1-5)}$$
Tiers are assigned as:
- `1 - 5`: Low
- `6 - 10`: Medium
- `11 - 15`: High
- `16 - 25`: Critical

### 3. Integrated Sidebar Filters
Filters applied globally cascade to relevant datasets:
- Selecting a **Department** filters controls, risks, audit findings, and vendors.
- Audit finding filters automatically cascade to isolate corresponding tasks in the remediation pipeline.

## Features

*   **KPI Overview**: Scorecards outlining active failures, open findings, compliance percentages, and critical items.
*   **Controls Tracker**: Full database of controls with dates and a quick form to update status (persisted back to the local CSVs).
*   **Risk Registry & Map**: Plotly 5x5 density heat map displaying risk distribution, with a form to log new risks.
*   **Audit & Action Pipeline**: Aging charts for audit findings and progress indicators mapping out resolved vs. overdue actions.
*   **Third-Party Vendors**: Expiry calendars, approvals, and data sensitivity ratings.
*   **Report Exporter**: Visualizes the active GRC metrics inside a copy-pasteable markdown advisor block with download utilities.

## Getting Started

### Installation
1. Navigate to the project directory:
   ```bash
   cd iso27001-grc-dashboard
   ```

2. Setup a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```
*Note: If data CSVs are not present under `data/`, the application will auto-run the synthetic generator to build standard sample files.*
