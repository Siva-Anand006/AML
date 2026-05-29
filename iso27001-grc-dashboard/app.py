import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os

# Set page configuration first
st.set_page_config(
    page_title="ISO 27001 GRC Cockpit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force imports from local package
from src.data_loader import load_all_data, save_dataframe_to_disk
from src.risk_scoring import calculate_risk_score, determine_risk_level, get_risk_color
from src.compliance_metrics import get_summary_kpis
from src.report_generator import generate_executive_report

# Custom styling for premium aesthetic
st.markdown("""
<style>
    .kpi-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    .kpi-title {
        font-size: 14px;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 28px;
        color: #1E293B;
        font-weight: 800;
    }
    .kpi-card-failed { border-left-color: #DC2626; }
    .kpi-card-open { border-left-color: #EA580C; }
    .kpi-card-overdue { border-left-color: #EF4444; }
    .kpi-card-critical { border-left-color: #B91C1C; }
    .kpi-card-compliance { border-left-color: #059669; }
</style>
""", unsafe_scale=True, unsafe_allow_html=True)

# 1. Load Data
dfs = load_all_data()

# 2. Extract Raw DataFrames
df_controls_raw = st.session_state.df_controls
df_risks_raw = st.session_state.df_risks
df_audit_findings_raw = st.session_state.df_audit_findings
df_remediation_raw = st.session_state.df_remediation
df_vendors_raw = st.session_state.df_vendors

# 3. Sidebar Filtering Panel
st.sidebar.title("🛡️ GRC Filters & Nav")

# Sidebar navigation
navigation_options = [
    "Executive Cockpit",
    "ISO 27001 Controls",
    "Risk Register",
    "Internal Audit Findings",
    "Remediation Tracker",
    "Vendor Risk Management",
    "Executive Report Builder"
]
selected_view = st.sidebar.selectbox("Go To Module", navigation_options)

st.sidebar.divider()
st.sidebar.subheader("Cross-Filtering Engine")

# Filter A: Department
all_departments = sorted(list(set(
    df_controls_raw["Department"].dropna().tolist() + 
    df_risks_raw["Department"].dropna().tolist() + 
    df_audit_findings_raw["Department"].dropna().tolist() + 
    df_vendors_raw["Department"].dropna().tolist()
)))
selected_dept = st.sidebar.selectbox("Filter Department", ["All"] + all_departments)

# Filter B: Risk Level
selected_risk_level = st.sidebar.selectbox("Filter Risk Level", ["All", "Low", "Medium", "High", "Critical"])

# Filter C: Control Status
selected_ctrl_status = st.sidebar.selectbox("Filter Control Status", ["All", "Compliant", "Partially Compliant", "Non-Compliant"])

# Filter D: Audit Finding Status
selected_finding_status = st.sidebar.selectbox("Filter Audit Finding Status", ["All", "Open", "In Progress", "Closed", "Overdue"])

# Filter E: Vendor Risk Rating
selected_vendor_risk = st.sidebar.selectbox("Filter Vendor Risk Rating", ["All", "Low", "Medium", "High", "Critical"])

# 4. Apply Filters (Local copies for display)
df_controls = df_controls_raw.copy()
df_risks = df_risks_raw.copy()
df_findings = df_audit_findings_raw.copy()
df_remediation = df_remediation_raw.copy()
df_vendors = df_vendors_raw.copy()

# Apply Department filter
if selected_dept != "All":
    df_controls = df_controls[df_controls["Department"] == selected_dept]
    df_risks = df_risks[df_risks["Department"] == selected_dept]
    df_findings = df_findings[df_findings["Department"] == selected_dept]
    df_vendors = df_vendors[df_vendors["Department"] == selected_dept]
    
    # Cascade department filter to remediation through related findings
    allowed_findings = df_audit_findings_raw[df_audit_findings_raw["Department"] == selected_dept]["Finding ID"].tolist()
    df_remediation = df_remediation[df_remediation["Related Finding ID"].isin(allowed_findings)]

# Apply Control Status filter
if selected_ctrl_status != "All":
    df_controls = df_controls[df_controls["Status"] == selected_ctrl_status]

# Apply Risk Level filter
if selected_risk_level != "All":
    df_risks = df_risks[df_risks["Risk Level"] == selected_risk_level]

# Apply Audit Finding Status filter
if selected_finding_status != "All":
    df_findings = df_findings[df_findings["Status"] == selected_finding_status]
    
    # Cascade to remediation
    allowed_findings = df_audit_findings_raw[df_audit_findings_raw["Status"] == selected_finding_status]["Finding ID"].tolist()
    df_remediation = df_remediation[df_remediation["Related Finding ID"].isin(allowed_findings)]

# Apply Vendor Risk Rating filter
if selected_vendor_risk != "All":
    df_vendors = df_vendors[df_vendors["Risk Rating"] == selected_vendor_risk]

# 5. Compute Active KPIs based on filtered datasets
kpis = get_summary_kpis({
    "controls": df_controls,
    "risks": df_risks,
    "audit_findings": df_findings,
    "remediation": df_remediation
})

# App Header
st.title("ISO 27001 GRC & Internal Audit Monitoring Cockpit")
st.caption("Strategic real-time auditing, quantitative risk logging, and continuous compliance evaluation.")
st.divider()

# ==========================================
# MODULE 1: EXECUTIVE COCKPIT
# ==========================================
if selected_view == "Executive Cockpit":
    st.subheader("Enterprise GRC Executive Cockpit")
    
    # Grid of KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""<div class="kpi-card kpi-card-compliance">
            <div class="kpi-title">Compliance Score</div>
            <div class="kpi-value">{kpis['compliance_score']}%</div>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Total Controls</div>
            <div class="kpi-value">{kpis['total_controls']}</div>
        </div>""", unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""<div class="kpi-card kpi-card-failed">
            <div class="kpi-title">Failed Controls</div>
            <div class="kpi-value">{kpis['failed_controls']}</div>
        </div>""", unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""<div class="kpi-card kpi-card-open">
            <div class="kpi-title">Open Findings</div>
            <div class="kpi-value">{kpis['open_findings']}</div>
        </div>""", unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""<div class="kpi-card kpi-card-overdue">
            <div class="kpi-title">Overdue Actions</div>
            <div class="kpi-value">{kpis['overdue_remediations']}</div>
        </div>""", unsafe_allow_html=True)
        
    with col6:
        st.markdown(f"""<div class="kpi-card kpi-card-critical">
            <div class="kpi-title">Critical Risks</div>
            <div class="kpi-value">{kpis['critical_risks']}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    
    # Visualizations row
    v_col1, v_col2 = st.columns([1, 1])
    
    with v_col1:
        # Donut Chart: Controls
        if not df_controls.empty:
            ctrl_counts = df_controls["Status"].value_counts().reset_index()
            ctrl_counts.columns = ["Status", "Count"]
            
            # Map colors
            color_map = {
                "Compliant": "#059669",
                "Partially Compliant": "#D97706",
                "Non-Compliant": "#DC2626"
            }
            
            fig_ctrls = px.pie(
                ctrl_counts, 
                names="Status", 
                values="Count", 
                hole=0.5,
                color="Status",
                color_discrete_map=color_map,
                title="ISO 27001 Control Health Breakdown"
            )
            fig_ctrls.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
            st.plotly_chart(fig_ctrls, use_container_width=True)
        else:
            st.info("No control data fits current filters.")
            
    with v_col2:
        # Speedometer Gauge: Compliance Score
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = kpis['compliance_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Compliance Speedometer Index", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1E3A8A"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#FEE2E2'},
                    {'range': [50, 80], 'color': '#FEF3C7'},
                    {'range': [80, 100], 'color': '#D1FAE5'}
                ]
            }
        ))
        fig_gauge.update_layout(margin=dict(t=50, b=20, l=40, r=40))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.divider()
    
    # Second Row of Visualizations
    v_col3, v_col4 = st.columns([1, 1])
    
    with v_col3:
        # Bar: Risks by Department
        if not df_risks.empty:
            dept_risk = df_risks.groupby("Department")["Risk Score"].mean().reset_index()
            dept_risk = dept_risk.sort_values(by="Risk Score", ascending=False)
            
            fig_dept_risk = px.bar(
                dept_risk,
                x="Department",
                y="Risk Score",
                color="Risk Score",
                color_continuous_scale="Reds",
                title="Average Quantitative Risk Score by Department"
            )
            st.plotly_chart(fig_dept_risk, use_container_width=True)
        else:
            st.info("No risk register data fits current filters.")
            
    with v_col4:
        # Stacked Bar: Audit Findings by Department & Severity
        if not df_findings.empty:
            findings_grouped = df_findings.groupby(["Department", "Severity"]).size().reset_index(name="Findings Count")
            
            color_sev_map = {
                "Low": "#059669",
                "Medium": "#D97706",
                "High": "#EA580C",
                "Critical": "#DC2626"
            }
            
            fig_findings = px.bar(
                findings_grouped,
                x="Department",
                y="Findings Count",
                color="Severity",
                color_discrete_map=color_sev_map,
                barmode="stack",
                title="Audit Findings Volume by Department & Severity"
            )
            st.plotly_chart(fig_findings, use_container_width=True)
        else:
            st.info("No audit findings fit current filters.")

# ==========================================
# MODULE 2: ISO 27001 CONTROLS
# ==========================================
elif selected_view == "ISO 27001 Controls":
    st.subheader("ISO 27001 Controls Monitoring Matrix")
    
    t_col1, t_col2 = st.columns([2, 1])
    
    with t_col1:
        st.write("### Active Controls Database")
        st.dataframe(df_controls, use_container_width=True)
        
        # Sub-tables: non-compliant or due
        non_compliant_ctrls = df_controls[df_controls["Status"] == "Non-Compliant"]
        if not non_compliant_ctrls.empty:
            st.warning("⚠️ **Active Non-Compliant Controls Requiring Intervention:**")
            st.dataframe(non_compliant_ctrls[["Control ID", "Control Name", "ISO 27001 Clause", "Department", "Control Owner"]], use_container_width=True)
            
    with t_col2:
        st.write("### Control Health Metrics")
        compliant_cnt = len(df_controls[df_controls["Status"] == "Compliant"])
        partial_cnt = len(df_controls[df_controls["Status"] == "Partially Compliant"])
        failed_cnt = len(df_controls[df_controls["Status"] == "Non-Compliant"])
        
        st.metric("Compliant Controls", compliant_cnt)
        st.metric("Partially Compliant Controls", partial_cnt)
        st.metric("Non-Compliant Controls", failed_cnt)
        
        st.divider()
        st.write("### ✏️ Quick Audit Update")
        with st.form("update_control_form"):
            control_to_update = st.selectbox("Select Control ID to Update", df_controls_raw["Control ID"].tolist())
            new_status = st.selectbox("Assign Status", ["Compliant", "Partially Compliant", "Non-Compliant"])
            submit_update = st.form_submit_button("Flush Audit Change")
            
            if submit_update:
                st.session_state.df_controls.loc[
                    st.session_state.df_controls["Control ID"] == control_to_update, "Status"
                ] = new_status
                
                # Update next/last review dates automatically to today
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                next_year_str = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
                st.session_state.df_controls.loc[
                    st.session_state.df_controls["Control ID"] == control_to_update, "Last Review Date"
                ] = today_str
                st.session_state.df_controls.loc[
                    st.session_state.df_controls["Control ID"] == control_to_update, "Next Review Date"
                ] = next_year_str
                
                save_dataframe_to_disk("controls")
                st.success(f"Control {control_to_update} status set to {new_status}. Changes persistent.")
                st.rerun()

# ==========================================
# MODULE 3: RISK REGISTER
# ==========================================
elif selected_view == "Risk Register":
    st.subheader("Enterprise Risk Register & Heat Map")
    
    r_col1, r_col2 = st.columns([1, 1])
    
    with r_col1:
        st.write("### 5x5 ISO 27005 Likelihood vs Impact Matrix")
        # Build 5x5 Likelihood / Impact Risk Heat Map
        import numpy as np
        matrix = np.zeros((5, 5), dtype=int)
        for _, row in df_risks.iterrows():
            try:
                l = int(row["Likelihood"]) - 1
                i = int(row["Impact"]) - 1
                if 0 <= l < 5 and 0 <= i < 5:
                    matrix[l, i] += 1
            except:
                pass
                
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=matrix,
            x=['1 (Very Low)', '2 (Low)', '3 (Medium)', '4 (High)', '5 (Very High)'],
            y=['1 (Very Low)', '2 (Low)', '3 (Medium)', '4 (High)', '5 (Very High)'],
            colorscale='YlOrRd',
            text=matrix,
            texttemplate="%{text}",
            hoverinfo='text'
        ))
        fig_heatmap.update_layout(
            xaxis_title="Quantitative Impact Severity", 
            yaxis_title="Quantitative Likelihood Score",
            margin=dict(l=40, r=40, t=20, b=40)
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
    with r_col2:
        st.write("### Log New Risk Vector")
        with st.form("new_risk_form"):
            r_name = st.text_input("Risk Scenario Title")
            r_dept = st.selectbox("Responsible Department", all_departments)
            r_like = st.slider("Likelihood Rating (1-5)", 1, 5, 3)
            r_imp = st.slider("Impact Rating (1-5)", 1, 5, 3)
            r_owner = st.text_input("Risk Owner Name")
            r_plan = st.text_area("Technical Mitigation Action Plan")
            
            submit_risk = st.form_submit_button("Commit Risk to Register")
            
            if submit_risk:
                if not r_name or not r_owner:
                    st.error("Fields cannot be left blank.")
                else:
                    new_score = calculate_risk_score(r_like, r_imp)
                    new_level = determine_risk_level(new_score)
                    
                    new_id = f"RSK-{len(df_risks_raw) + 1:02d}"
                    
                    new_row = {
                        "Risk ID": new_id,
                        "Risk Name": r_name,
                        "Department": r_dept,
                        "Likelihood": r_like,
                        "Impact": r_imp,
                        "Risk Score": new_score,
                        "Risk Level": new_level,
                        "Risk Owner": r_owner,
                        "Mitigation Plan": r_plan
                    }
                    
                    st.session_state.df_risks = pd.concat([df_risks_raw, pd.DataFrame([new_row])], ignore_index=True)
                    save_dataframe_to_disk("risks")
                    st.success(f"Risk {new_id} added successfully.")
                    st.rerun()

    st.divider()
    st.write("### Registered Risk Vector Ledger")
    st.dataframe(df_risks, use_container_width=True)

# ==========================================
# MODULE 4: INTERNAL AUDIT FINDINGS
# ==========================================
elif selected_view == "Internal Audit Findings":
    st.subheader("Internal Audit Findings Ledger & Aging Review")
    
    aud_col1, aud_col2 = st.columns([3, 1])
    
    with aud_col1:
        st.write("### Active Audit Findings")
        st.dataframe(df_findings, use_container_width=True)
        
        # Overdue Findings list
        overdue_findings = df_findings[df_findings["Status"] == "Overdue"]
        if not overdue_findings.empty:
            st.error("🚨 **Overdue Security Findings Requiring Immediate Attention:**")
            st.dataframe(overdue_findings, use_container_width=True)
            
    with aud_col2:
        st.write("### Audit Summary Metrics")
        open_findings_cnt = len(df_findings[df_findings["Status"] != "Closed"])
        avg_days_open = df_findings[df_findings["Status"] != "Closed"]["Days Open"].mean() if open_findings_cnt > 0 else 0
        
        st.metric("Open Findings", open_findings_cnt)
        st.metric("Avg Days Open (Active)", f"{avg_days_open:.1f} Days")
        
        st.divider()
        st.write("### ✏️ Audit Finding Status Update")
        with st.form("update_finding_form"):
            finding_to_update = st.selectbox("Select Finding ID", df_audit_findings_raw["Finding ID"].tolist())
            new_status = st.selectbox("Assign Status", ["Open", "In Progress", "Closed", "Overdue"])
            submit_finding_update = st.form_submit_button("Commit Status Update")
            
            if submit_finding_update:
                st.session_state.df_audit_findings.loc[
                    st.session_state.df_audit_findings["Finding ID"] == finding_to_update, "Status"
                ] = new_status
                save_dataframe_to_disk("audit_findings")
                st.success(f"Finding {finding_to_update} updated to {new_status}.")
                st.rerun()

# ==========================================
# MODULE 5: REMEDIATION TRACKER
# ==========================================
elif selected_view == "Remediation Tracker":
    st.subheader("Actionable Remediation Progress tracker")
    
    rem_col1, rem_col2 = st.columns([3, 1])
    
    with rem_col1:
        st.write("### Scheduled Remediation Pipeline")
        st.dataframe(df_remediation, use_container_width=True)
        
        # Display overdue tasks
        overdue_actions = df_remediation[df_remediation["Status"] == "Overdue"]
        if not overdue_actions.empty:
            st.error("⚠️ **Critical Overdue Action Items:**")
            st.dataframe(overdue_actions, use_container_width=True)
            
    with rem_col2:
        st.write("### Mitigation Performance Indicators")
        total_actions = len(df_remediation)
        completed_actions = len(df_remediation[df_remediation["Status"] == "Completed"])
        
        progress_pct = (completed_actions / total_actions) if total_actions > 0 else 1.0
        
        st.write("#### Closed Remediation Rates")
        st.progress(progress_pct)
        st.write(f"**{completed_actions} / {total_actions} ({progress_pct*100:.1f}%)** actions completed.")
        
        st.divider()
        st.write("### ✏️ Remediation Update Form")
        with st.form("update_remediation_form"):
            action_to_update = st.selectbox("Select Action ID", df_remediation_raw["Action ID"].tolist())
            new_rem_status = st.selectbox("Action Status", ["Not Started", "In Progress", "Completed", "Overdue"])
            submit_rem_update = st.form_submit_button("Flush Action Change")
            
            if submit_rem_update:
                st.session_state.df_remediation.loc[
                    st.session_state.df_remediation["Action ID"] == action_to_update, "Status"
                ] = new_rem_status
                save_dataframe_to_disk("remediation")
                st.success(f"Remediation action {action_to_update} set to {new_rem_status}.")
                st.rerun()

# ==========================================
# MODULE 6: VENDOR RISK MANAGEMENT
# ==========================================
elif selected_view == "Vendor Risk Management":
    st.subheader("Third-Party Vendor Risk Matrix")
    
    v_col1, v_col2 = st.columns([3, 1])
    
    with v_col1:
        st.write("### Third-Party Processor Ledger")
        st.dataframe(df_vendors, use_container_width=True)
        
        # High Risk vendors sub-ledger
        high_risk_v = df_vendors[df_vendors["Risk Rating"].isin(["High", "Critical"])]
        if not high_risk_v.empty:
            st.warning("🚨 **High Risk Processors Requiring SOC 2 Verification:**")
            st.dataframe(high_risk_v[["Vendor ID", "Vendor Name", "Service Type", "Data Sensitivity", "Risk Rating", "Status"]], use_container_width=True)
            
    with v_col2:
        st.write("### Third-Party Exposure Indicators")
        total_v = len(df_vendors)
        hr_count = len(df_vendors[df_vendors["Risk Rating"].isin(["High", "Critical"])])
        app_count = len(df_vendors[df_vendors["Status"] == "Approved"])
        
        st.metric("Total Third Parties", total_v)
        st.metric("High/Critical Risk Vendors", hr_count)
        st.metric("Vendor Approval Rate", f"{(app_count/total_v)*100:.0f}%" if total_v > 0 else "100%")
        
        st.divider()
        st.write("### ✏️ Edit Vendor Profile")
        with st.form("edit_vendor_form"):
            vendor_to_update = st.selectbox("Select Vendor ID", df_vendors_raw["Vendor ID"].tolist())
            new_v_rating = st.selectbox("Risk Rating", ["Low", "Medium", "High", "Critical"])
            new_v_status = st.selectbox("Approval Status", ["Approved", "Review Required", "High Risk"])
            submit_vendor_update = st.form_submit_button("Flush Profile Change")
            
            if submit_vendor_update:
                st.session_state.df_vendors.loc[
                    st.session_state.df_vendors["Vendor ID"] == vendor_to_update, "Risk Rating"
                ] = new_v_rating
                st.session_state.df_vendors.loc[
                    st.session_state.df_vendors["Vendor ID"] == vendor_to_update, "Status"
                ] = new_v_status
                save_dataframe_to_disk("vendors")
                st.success(f"Vendor {vendor_to_update} updated.")
                st.rerun()

# ==========================================
# MODULE 7: EXECUTIVE REPORT BUILDER
# ==========================================
elif selected_view == "Executive Report Builder":
    st.subheader("Interactive Executive Report Builder")
    st.write("Generates a highly structured, regulatory-ready executive GRC summary report using current real-time dataset states.")
    
    # Generate report markdown
    report_content = generate_executive_report({
        "controls": df_controls,
        "risks": df_risks,
        "audit_findings": df_findings,
        "remediation": df_remediation,
        "vendors": df_vendors
    }, kpis)
    
    st.divider()
    st.markdown(report_content)
    st.divider()
    
    # Download report button
    st.download_button(
        label="📥 Download Executive GRC Report (Markdown)",
        data=report_content,
        file_name=f"ISO_27001_Executive_Report_{datetime.date.today().strftime('%Y_%m_%d')}.md",
        mime="text/markdown"
    )
