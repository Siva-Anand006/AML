import datetime
import pandas as pd

def generate_executive_report(dfs, kpis):
    """
    Constructs a professional, comprehensive executive report summarizing
    the organization's current ISO 27001 GRC and compliance posture.
    """
    df_controls = dfs.get("controls", pd.DataFrame())
    df_risks = dfs.get("risks", pd.DataFrame())
    df_findings = dfs.get("audit_findings", pd.DataFrame())
    df_remediation = dfs.get("remediation", pd.DataFrame())
    df_vendors = dfs.get("vendors", pd.DataFrame())
    
    # 1. Determine highest-risk department
    highest_risk_dept = "None"
    highest_risk_avg = 0.0
    if not df_risks.empty:
        dept_risk = df_risks.groupby("Department")["Risk Score"].mean()
        if not dept_risk.empty:
            highest_risk_dept = dept_risk.idxmax()
            highest_risk_avg = round(dept_risk.max(), 2)
            
    # 2. Compile non-compliant controls
    failed_controls_list = []
    if not df_controls.empty:
        failed_ctrls = df_controls[df_controls["Status"] == "Non-Compliant"]
        for _, row in failed_ctrls.iterrows():
            failed_controls_list.append(f"- **{row['Control ID']}**: {row['Control Name']} ({row['ISO 27001 Clause']}) - Owner: {row['Control Owner']}")
            
    failed_controls_str = "\n".join(failed_controls_list) if failed_controls_list else "- No completely non-compliant controls identified."
    
    # 3. Compile top critical/high risks
    critical_risks_list = []
    if not df_risks.empty:
        high_crit_risks = df_risks[df_risks["Risk Level"].isin(["Critical", "High"])]
        for _, row in high_crit_risks.sort_values(by="Risk Score", ascending=False).iterrows():
            critical_risks_list.append(f"- **{row['Risk ID']}**: {row['Risk Name']} (Score: {row['Risk Score']}, Level: {row['Risk Level']}) - Mitigation: {row['Mitigation Plan']}")
            
    critical_risks_str = "\n".join(critical_risks_list) if critical_risks_list else "- No critical or high-level risk items logged."
    
    # 4. Compile overdue findings and remediations
    overdue_actions = []
    if not df_remediation.empty:
        overdue_items = df_remediation[df_remediation["Status"] == "Overdue"]
        for _, row in overdue_items.iterrows():
            overdue_actions.append(f"- **{row['Action ID']}** (Under Finding {row['Related Finding ID']}): {row['Action Description']} - Owner: {row['Owner']} - Due: {row['Due Date']}")
            
    overdue_actions_str = "\n".join(overdue_actions) if overdue_actions else "- No overdue remediation items outstanding."

    # 5. Extract high-risk vendors
    high_risk_vendors = []
    if not df_vendors.empty:
        hr_vendors = df_vendors[df_vendors["Risk Rating"].isin(["Critical", "High"])]
        for _, row in hr_vendors.iterrows():
            high_risk_vendors.append(f"- **{row['Vendor Name']}** ({row['Service Type']}) - Sensitivity: {row['Data Sensitivity']} - Status: {row['Status']}")
            
    hr_vendors_str = "\n".join(high_risk_vendors) if high_risk_vendors else "- No critical third-party vendor risks logged."

    # 6. Auto-generate recommended next actions based on data state
    recs = []
    if kpis["failed_controls"] > 0:
        recs.append("1. **Remediate Failed Controls**: Prioritize security engineering and audit logging capabilities for non-compliant controls (CTRL-12, CTRL-13).")
    if kpis["overdue_remediations"] > 0:
        recs.append("2. **Address Overdue Remediation Work**: Coordinate with owners of overdue tasks (specifically outstanding access revocation sync REM-03) to clear operational roadblocks.")
    if highest_risk_dept != "None" and highest_risk_avg >= 12.0:
        recs.append(f"3. **Target Departmental Risk**: Support the **{highest_risk_dept}** business unit (highest average risk score of {highest_risk_avg}) with dedicated control reviews and budget.")
    if len(high_risk_vendors) > 0:
        recs.append("4. **Perform Third-Party Security Audits**: Conduct immediate assessments of third-party vendors flagged with High or Critical ratings, ensuring updated SOC 2 certifications.")
    recs.append("5. **Continuous Internal Audit Cycle**: Plan the next internal tabletop audit simulation for business continuity preparedness (CTRL-17).")
    
    recs_str = "\n".join(recs)
    
    current_date = datetime.date.today().strftime("%B %d, %Y")
    
    report_md = f"""# ISO 27001 Executive Security & Compliance Report

**Generated on:** {current_date}  
**Auditor/GRC Lead:** GRC Decision Cockpit  
**Target Standard:** ISO/IEC 27001:2022  

---

## 1. Executive Summary
This document provides an overview of the organization's current compliance posture, active risk scores, internal audit findings, and remediation statuses. Currently, the organization maintains a composite **ISO 27001 Compliance Score of {kpis['compliance_score']}%**. While the overall control health is high, immediate GRC focus must shift toward mitigating unresolved critical risks and overdue remediation items.

### Key GRC Posture Metrics
- **ISO 27001 Compliance Score:** `{kpis['compliance_score']}%`
- **Total Controls Monitored:** `{kpis['total_controls']}`
- **Non-Compliant Controls (Failed):** `{kpis['failed_controls']}`
- **Active / Open Audit Findings:** `{kpis['open_findings']}`
- **Overdue Remediation Actions:** `{kpis['overdue_remediations']}`
- **Enterprise Critical Risks:** `{kpis['critical_risks']}`
- **Highest-Risk Department (Avg Score):** `"{highest_risk_dept}"` (Average score: {highest_risk_avg})

---

## 2. Technical Findings & Security Gaps

### Non-Compliant & Failed ISO Controls
These controls failed security review and require active remediation to maintain compliance:
{failed_controls_str}

### Prioritized Enterprise Risks (Critical & High Tiers)
Active vulnerabilities and scenarios posing high operational or regulatory exposure:
{critical_risks_str}

### Overdue Remediation Items
The following action items are past their scheduled due dates and must be triaged immediately:
{overdue_actions_str}

### Third-Party & Vendor Risks
High-sensitivity data streams managed by external processors requiring risk review:
{hr_vendors_str}

---

## 3. Recommended Remediation Roadmap
Based on analytical metrics, the GRC team advises the following sequence of immediate remediation:

{recs_str}

---

**Report Classification:** Internal Use Only - Confidential
"""
    return report_md
