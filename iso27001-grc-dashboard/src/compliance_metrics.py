import pandas as pd

def calculate_compliance_score(df_controls):
    """
    Computes ISO 27001 compliance score using standard weighted formula:
    (Compliant + 0.5 * Partially Compliant) / Total Controls * 100
    """
    if df_controls.empty:
        return 100.0
        
    total = len(df_controls)
    compliant = len(df_controls[df_controls["Status"] == "Compliant"])
    partial = len(df_controls[df_controls["Status"] == "Partially Compliant"])
    
    score = ((compliant + (0.5 * partial)) / total) * 100.0
    return round(score, 1)

def get_summary_kpis(dfs):
    """
    Computes primary compliance, risk, and audit key performance indicators (KPIs)
    from all GRC tables.
    """
    df_controls = dfs.get("controls", pd.DataFrame())
    df_risks = dfs.get("risks", pd.DataFrame())
    df_findings = dfs.get("audit_findings", pd.DataFrame())
    df_remediation = dfs.get("remediation", pd.DataFrame())
    
    # 1. ISO Compliance Score
    compliance_score = calculate_compliance_score(df_controls)
    
    # 2. Total Controls
    total_controls = len(df_controls)
    
    # 3. Failed Controls (Non-Compliant)
    failed_controls = len(df_controls[df_controls["Status"] == "Non-Compliant"]) if not df_controls.empty else 0
    
    # 4. Open Audit Findings (Non-Closed)
    open_findings = len(df_findings[df_findings["Status"] != "Closed"]) if not df_findings.empty else 0
    
    # 5. Critical Risks (Level is Critical)
    critical_risks = len(df_risks[df_risks["Risk Level"] == "Critical"]) if not df_risks.empty else 0
    
    # 6. Overdue Remediation Items (Status is Overdue)
    overdue_remediations = len(df_remediation[df_remediation["Status"] == "Overdue"]) if not df_remediation.empty else 0
    
    return {
        "compliance_score": compliance_score,
        "total_controls": total_controls,
        "failed_controls": failed_controls,
        "open_findings": open_findings,
        "critical_risks": critical_risks,
        "overdue_remediations": overdue_remediations
    }
