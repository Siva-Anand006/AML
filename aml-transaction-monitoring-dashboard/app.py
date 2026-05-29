import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from src.data_loader import load_data, standardize_columns
from src.rules_engine import apply_aml_rules
from src.risk_scoring import calculate_risk_score
from src.case_report import generate_case_summary
from src.synthetic_generator import generate_synthetic_aml_data

# Set page config with dark themes/wide layout in mind
st.set_page_config(
    page_title="AML Transaction Monitoring Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling for dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Main body background and fonts */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header and Title custom styling */
    .premium-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .premium-caption {
        font-size: 1rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    
    /* Custom metric card layout (Glassmorphism card aesthetic) */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 20px;
    }
    .kpi-card {
        flex: 1;
        min-width: 180px;
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 5px;
    }
    .kpi-indicator {
        width: 35px;
        height: 4px;
        border-radius: 2px;
        margin-top: 10px;
    }
    
    /* Custom CSS to style elements */
    .stDownloadButton button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stDownloadButton button:hover {
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Data manager cache
@st.cache_data
def get_processed_data():
    csv_path = "data/aml_transactions.csv"
    
    # Auto-generate if missing
    if not os.path.exists(csv_path):
        os.makedirs("data", exist_ok=True)
        generate_synthetic_aml_data(csv_path, num_rows=15000)
        
    df = load_data(csv_path)
    df = standardize_columns(df)
    df = apply_aml_rules(df)
    df = calculate_risk_score(df)
    return df

try:
    df = get_processed_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.info("Generating a fresh dataset to recover...")
    csv_path = "data/aml_transactions.csv"
    os.makedirs("data", exist_ok=True)
    generate_synthetic_aml_data(csv_path, num_rows=15000)
    df = get_processed_data()

# Header Section
st.markdown('<div class="premium-title">🛡️ AML Transaction Monitoring & Suspicious Activity Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-caption">Interactive risk scoring, real-time alert prioritization, and compliance report generation cockpit.</div>', unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h3 style='color: #F8FAFC; font-weight: 700; margin: 0;'>🎛️ Control Panel</h3>
        <p style='color: #94A3B8; font-size: 0.85rem;'>Configure transaction monitoring criteria</p>
        <hr style='border-color: rgba(255,255,255,0.1); margin-top: 10px; margin-bottom: 10px;' />
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("Risk Settings")

risk_options = list(df["risk_level"].dropna().unique())
# Sort by order of levels
level_order = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
risk_options = sorted(risk_options, key=lambda x: level_order.get(x, 4))

risk_levels = st.sidebar.multiselect(
    "Risk Level Tiers",
    options=risk_options,
    default=risk_options
)

transaction_types = st.sidebar.multiselect(
    "Transaction Type",
    options=list(df["transaction_type"].dropna().unique()),
    default=list(df["transaction_type"].dropna().unique())
)

min_val = float(df["amount"].min())
max_val = float(df["amount"].max())

# Cap filters to log scale or reasonable standard to improve slide control
min_amount, max_amount = st.sidebar.slider(
    "Transaction Amount ($)",
    min_val,
    max_val,
    (min_val, max_val),
    format="$%d"
)

# Apply filters reactively
filtered_df = df[
    (df["risk_level"].isin(risk_levels)) &
    (df["transaction_type"].isin(transaction_types)) &
    (df["amount"].between(min_amount, max_amount))
]

alerts_df = filtered_df[filtered_df["is_alert"] == True]

# Calculations for metrics
total_transactions = len(filtered_df)
total_alerts = len(alerts_df)
alert_rate = (total_alerts / total_transactions * 100) if total_transactions else 0
suspicious_value = alerts_df["amount"].sum()
high_risk_customers = alerts_df["sender"].nunique()

# Render custom KPI Cards using HSL colors & HTML
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Total Transactions</div>
            <div class="kpi-value">{total_transactions:,}</div>
            <div class="kpi-indicator" style="background: #3B82F6;"></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">AML Alerts Triggered</div>
            <div class="kpi-value">{total_alerts:,}</div>
            <div class="kpi-indicator" style="background: #EF4444;"></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Alert Rate</div>
            <div class="kpi-value">{alert_rate:.2f}%</div>
            <div class="kpi-indicator" style="background: #F59E0B;"></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Suspicious Volume</div>
            <div class="kpi-value">${suspicious_value:,.2f}</div>
            <div class="kpi-indicator" style="background: #10B981;"></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">High-Risk Accounts</div>
            <div class="kpi-value">{high_risk_customers:,}</div>
            <div class="kpi-indicator" style="background: #8B5CF6;"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Charts Section
left_col, right_col = st.columns(2)

# Customized dark layout themes for Plotly
plotly_layout = dict(
    paper_bgcolor="rgba(17, 24, 39, 0.7)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E2E8F0",
    font_family="'Outfit', sans-serif",
    margin=dict(l=40, r=40, t=50, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
)

with left_col:
    # 1. Transactions by Risk Level (Bar Chart)
    risk_counts = filtered_df["risk_level"].value_counts().reindex(["Low", "Medium", "High", "Critical"]).fillna(0).reset_index()
    risk_counts.columns = ["Risk Level", "Volume"]
    
    # Matching CSS Palette colors
    risk_colors = {
        "Low": "#10B981",       # Emerald Green
        "Medium": "#F59E0B",    # Amber Orange
        "High": "#EF4444",      # Crimson Red
        "Critical": "#8B5CF6"   # Violet Purple
    }
    
    fig_risk = px.bar(
        risk_counts,
        x="Risk Level",
        y="Volume",
        color="Risk Level",
        color_discrete_map=risk_colors,
        title="Transaction Volumes by Assigned Risk Tier"
    )
    fig_risk.update_layout(**plotly_layout)
    st.plotly_chart(fig_risk, use_container_width=True)

with right_col:
    # 2. Transaction Value by Type (Donut Chart)
    type_chart = filtered_df.groupby("transaction_type")["amount"].sum().reset_index()
    type_chart.columns = ["Type", "Total Value ($)"]
    
    fig_type = px.pie(
        type_chart,
        names="Type",
        values="Total Value ($)",
        hole=0.45,
        title="Aggregate Transaction Value by Transfer Method",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_type.update_layout(**plotly_layout)
    st.plotly_chart(fig_type, use_container_width=True)

# 3. AML Rule Trigger Summary (Full-Width Chart)
st.markdown("### 📊 AML Detection Rule Infractions")
rule_cols = [
    "rule_high_value",
    "rule_unusual_amount",
    "rule_high_velocity",
    "rule_structuring",
    "rule_high_total_sender_value",
    "rule_high_risk_country",
]

rule_labels = {
    "rule_high_value": "High-Value Transfer",
    "rule_unusual_amount": "Amount Spike (3x Avg)",
    "rule_high_velocity": "High Frequency",
    "rule_structuring": "Structuring ($9k-$10k)",
    "rule_high_total_sender_value": "High Total Sender Vol",
    "rule_high_risk_country": "High-Risk Geography Link"
}

rule_summary = pd.DataFrame({
    "Rule Indicator": [rule_labels[col] for col in rule_cols],
    "Occurrences": [filtered_df[col].sum() for col in rule_cols]
}).sort_values("Occurrences", ascending=True)

fig_rules = px.bar(
    rule_summary,
    x="Occurrences",
    y="Rule Indicator",
    orientation="h",
    title="Rule Violation Frequencies Across Transactions",
    color="Occurrences",
    color_continuous_scale=px.colors.sequential.Sunsetdark
)
fig_rules.update_layout(**plotly_layout)
fig_rules.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig_rules, use_container_width=True)

st.markdown("---")

# alert table Queue
st.markdown("### 🔍 Alert Investigation & Review Queue")
st.caption("Transactions flagged for compliance audit based on risk score (>= 50). Use filters to narrow results.")

display_cols = [
    "timestamp",
    "sender",
    "receiver",
    "transaction_type",
    "amount",
    "risk_score",
    "risk_level",
    "rules_triggered",
    "is_laundering",
]

existing_display_cols = [col for col in display_cols if col in alerts_df.columns]

if len(alerts_df) > 0:
    # Sort by risk score (descending)
    sorted_alerts = alerts_df[existing_display_cols].sort_values("risk_score", ascending=False)
    
    st.dataframe(
        sorted_alerts,
        use_container_width=True,
        column_config={
            "amount": st.column_config.NumberColumn("Amount ($)", format="$%,.2f"),
            "risk_score": st.column_config.ProgressColumn("Risk Score (0-100)", min_value=0, max_value=100, format="%d"),
            "is_laundering": st.column_config.CheckboxColumn("Ground Truth (Laundering)"),
            "rules_triggered": st.column_config.NumberColumn("Violated Rules")
        }
    )
    
    # Export layout
    export_df = sorted_alerts.copy()
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    
    col_dl, col_spacer = st.columns([1, 4])
    with col_dl:
        st.download_button(
            label="💾 Download Review Queue (CSV)",
            data=csv_bytes,
            file_name="aml_flagged_alerts.csv",
            mime="text/csv"
        )
else:
    st.info("No active alerts found matching current control panel filters.")

st.markdown("---")

# Case Narrative Generator
st.markdown("### 📝 Compliance Narrative Case Generator")
st.caption("Select a flagged transaction from the active alerts queue to generate a formal investigation report.")

if len(alerts_df) > 0:
    # Generate list of alerts for dropdown selector
    alert_options = alerts_df.sort_values("risk_score", ascending=False).copy()
    alert_options["selector_label"] = (
        "Sender: " + alert_options["sender"].astype(str) + 
        " | Amt: $" + alert_options["amount"].map("{:,.2f}".format) + 
        " | Risk: " + alert_options["risk_score"].astype(str) + 
        " (Row: " + alert_options.index.astype(str) + ")"
    )
    
    selected_option = st.selectbox(
        "Select transaction alert to generate case report:",
        options=alert_options["selector_label"].tolist()
    )
    
    # Extract the original index from label (Row: XXX)
    selected_index = int(selected_option.split("(Row: ")[-1][:-1])
    selected_row = alerts_df.loc[selected_index]
    
    case_summary = generate_case_summary(selected_row)
    
    st.markdown("#### Generated Suspicious Activity Narrative Summary")
    st.text_area(
        "Copyable SAR Description",
        value=case_summary,
        height=180,
        help="Copy this text directly into suspicious activity reporting logs or case management notes."
    )
else:
    st.info("No alerts are available to report. Adjust control panel parameters to display alerts.")
