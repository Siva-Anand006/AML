# ISO 27001 GRC & Internal Audit Monitoring Platform

A professional, local Governance, Risk, and Compliance (GRC) platform designed to track and audit security controls, evaluate enterprise risk, monitor internal audit pipelines, and assess third-party vendor exposures. Built using Streamlit, Pandas, and Plotly, this platform serves as an interactive compliance decision engine modeled after industry-standard GRC toolsets.

---

## 🎯 Business Context & GRC Objectives

Organizations pursuing or maintaining **ISO/IEC 27001:2022** certification are required to establish systematic methods for monitoring control health (Clause 9.1), conducting internal audits (Clause 9.2), and executing risk treatment plans (Clause 6.2). 

Maintaining separate spreadsheets for controls, enterprise risk registers, internal audit findings, and vendor assessments often leads to fragmented visibility, disjointed filtering, and lagging remediation timelines. 

This platform unifies these workflows into a single compliance cockpit, offering:
1. **Real-time Compliance Indexes**: Dynamic calculation of control health percentages based on weighted compliance assessments.
2. **Unified Data Cross-Filtering**: Instant synchronization across separate datasets (e.g., viewing only the Engineering department's active controls, critical risks, open audit findings, and high-risk vendors simultaneously).
3. **Structured Remediation & Closing Lifecycles**: A collaborative interface allowing users to record, update, and persist control reviews, audit statuses, and risk mitigation plans directly to disk.
4. **Automated C-Suite Advisory Drafting**: An executive report builder that translates active dataset states into markdown security memos.

---

## 📁 Repository Structure

```
iso27001-grc-dashboard/
├── app.py                      # Streamlit application UI & modules layout
├── requirements.txt            # Project dependencies (Streamlit, Pandas, Plotly)
├── README.md                   # Technical documentation and deployment guide
├── data/                       # Local directory containing CSV data tables
│   ├── controls.csv            # Annex A control inventory
│   ├── risks.csv               # Quantitative risk register
│   ├── audit_findings.csv      # Audit issues database
│   ├── remediation.csv         # Action plan tracker
│   └── vendors.csv             # Third-party risk profiles
└── src/                        # Platform logic sub-packages
    ├── __init__.py
    ├── data_generator.py       # Deterministic realistic synthetic generator
    ├── data_loader.py          # Session-state state engine & persistence
    ├── risk_scoring.py         # Risk level calculations and matrix settings
    ├── compliance_metrics.py   # Aggregations, percentages, and metrics
    └── report_generator.py     # Executive report compiler
```

---

## ⚙️ Technical Architecture & Metrics Logic

### 1. ISO 27001 Control Health Index
The platform computes a composite health score based on the status of standard controls:
$$\text{Compliance Score (\%)} = \frac{\text{Compliant Controls} + (0.5 \times \text{Partially Compliant Controls})}{\text{Total Controls}} \times 100$$
Controls are categorized under standard **ISO 27001:2022** clauses (e.g., A.5 Organisational controls, A.7 Physical controls, A.8 Technological controls).

### 2. Quantitative Risk-Scoring Engine
Following ISO 27005 guidelines, risk exposure is modeled using likelihood and impact factors (rated 1 to 5):
$$\text{Risk Score} = \text{Likelihood} \times \text{Impact} \quad (\text{Range: } 1 - 25)$$
Scores are classified into standard priority levels:
- `1 - 5`: **Low** (Acceptable risk)
- `6 - 10`: **Medium** (Monitor with existing controls)
- `11 - 15`: **High** (Mitigate within scheduled development)
- `16 - 25`: **Critical** (Immediate escalation and mitigation)

### 3. Integrated Cross-Filtering
Filters applied in the sidebar cascade globally:
- Filtering by **Department** limits controls, risks, audit findings, and vendor registries to that specific business unit.
- Finding-to-remediation relationships are automatically resolved (e.g., filtering for a specific audit status isolates the related action items in the remediation tracker).

---

## 🚀 Key Dashboard Features

*   **Executive Dashboard**: Modern visual scorecards displaying high-priority KPIs, a Plotly Gauge speedometer of compliance health, and interactive charts plotting risk averages and audit volume by department.
*   **Controls Matrix**: Comprehensive ledger of regulatory controls with review dates and an interactive form allowing immediate status overrides that persist back to local CSV storage.
*   **Interactive Risk Register**: Features a 5x5 Plotly risk heat map counting scenarios residing in each likelihood-impact cell, alongside an entry form to log new threat vectors.
*   **Audit Aging & Remediation Tracker**: Analyzes finding severity distribution, visualizes action-completion progress bars, and highlights critical overdue tasks.
*   **Third-Party Vendor Module**: Identifies high-risk processors operating on sensitive datasets, monitors contract expiry timelines, and maps vendor status ratings.
*   **Report Generator**: Builds a structured markdown executive brief complete with target statistics and recommended roadmaps, ready for clipboard copying or file downloading.

---

## 🛠️ Installation & Execution Guide

### Prerequisites
*   Python 3.9 or higher

### Step-by-Step Launch
1. Navigate into the platform directory:
   ```bash
   cd iso27001-grc-dashboard
   ```

2. Establish and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```
*Note: If no datasets exist, the platform automatically generates realistic synthetic datasets inside `data/` upon launch.*

---

## 📝 Resume Bullet Point Highlights

**Governance, Risk & Compliance (GRC) Dashboard | Python, Streamlit, Pandas, Plotly**
*   Designed and built a modular GRC compliance dashboard simulating ISO 27001 audit workflows, risk registers, and third-party vendor monitoring.
*   Developed a dynamic risk-scoring model (Likelihood × Impact) and interactive 5x5 heat map using Plotly, allowing risk managers to identify and log security threat vectors.
*   Implemented a session-state-driven data load and write-back engine in Pandas to enable persistent database CRUD updates directly to underlying CSV storage.
*   Created an integrated cross-filtering controller to cascade department, risk, and control selections globally across separate relational data models, improving data query efficiency.
*   Integrated a dynamic markdown executive report compiler, translating active GRC metrics into structured compliance advisory briefs for leadership reviews.
