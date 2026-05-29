import os
import pandas as pd
import datetime

def generate_synthetic_data(data_dir):
    """
    Generates realistic GRC data for an ISO 27001 Audit and Compliance dashboard.
    """
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. ISO 27001 Controls
    controls_data = [
        {"Control ID": "CTRL-01", "Control Name": "Information Security Policies", "ISO 27001 Clause": "A.5.1", "Department": "Compliance", "Control Owner": "Sarah Jenkins", "Status": "Compliant", "Last Review Date": "2026-01-15", "Next Review Date": "2027-01-15"},
        {"Control ID": "CTRL-02", "Control Name": "Inventory of Assets", "ISO 27001 Clause": "A.5.9", "Department": "IT Operations", "Control Owner": "David Chen", "Status": "Compliant", "Last Review Date": "2026-02-10", "Next Review Date": "2027-02-10"},
        {"Control ID": "CTRL-03", "Control Name": "Access Control Policy", "ISO 27001 Clause": "A.5.15", "Department": "Information Security", "Control Owner": "Alex Mercer", "Status": "Compliant", "Last Review Date": "2026-03-01", "Next Review Date": "2027-03-01"},
        {"Control ID": "CTRL-04", "Control Name": "User Registration and De-registration", "ISO 27001 Clause": "A.5.16", "Department": "HR", "Control Owner": "Emma Watson", "Status": "Partially Compliant", "Last Review Date": "2025-11-20", "Next Review Date": "2026-05-20"},
        {"Control ID": "CTRL-05", "Control Name": "Use of Cryptographic Controls", "ISO 27001 Clause": "A.8.24", "Department": "Engineering", "Control Owner": "Marcus Vance", "Status": "Compliant", "Last Review Date": "2026-01-05", "Next Review Date": "2027-01-05"},
        {"Control ID": "CTRL-06", "Control Name": "Physical Security Perimeter", "ISO 27001 Clause": "A.7.1", "Department": "Facilities", "Control Owner": "John Miller", "Status": "Compliant", "Last Review Date": "2025-08-14", "Next Review Date": "2026-08-14"},
        {"Control ID": "CTRL-07", "Control Name": "Equipment Sitting and Protection", "ISO 27001 Clause": "A.7.6", "Department": "Facilities", "Control Owner": "John Miller", "Status": "Compliant", "Last Review Date": "2025-09-10", "Next Review Date": "2026-09-10"},
        {"Control ID": "CTRL-08", "Control Name": "Protection against Malware", "ISO 27001 Clause": "A.8.7", "Department": "IT Operations", "Control Owner": "David Chen", "Status": "Compliant", "Last Review Date": "2026-02-28", "Next Review Date": "2027-02-28"},
        {"Control ID": "CTRL-09", "Control Name": "Backup of Information", "ISO 27001 Clause": "A.8.13", "Department": "IT Operations", "Control Owner": "David Chen", "Status": "Compliant", "Last Review Date": "2026-04-12", "Next Review Date": "2027-04-12"},
        {"Control ID": "CTRL-10", "Control Name": "Network Controls & Security", "ISO 27001 Clause": "A.8.20", "Department": "Engineering", "Control Owner": "Marcus Vance", "Status": "Partially Compliant", "Last Review Date": "2025-10-18", "Next Review Date": "2026-04-18"},
        {"Control ID": "CTRL-11", "Control Name": "Information Transfer Policies", "ISO 27001 Clause": "A.8.11", "Department": "Compliance", "Control Owner": "Sarah Jenkins", "Status": "Compliant", "Last Review Date": "2026-02-18", "Next Review Date": "2027-02-18"},
        {"Control ID": "CTRL-12", "Control Name": "Security Activity Logging & Monitoring", "ISO 27001 Clause": "A.8.15", "Department": "Information Security", "Control Owner": "Alex Mercer", "Status": "Non-Compliant", "Last Review Date": "2025-05-15", "Next Review Date": "2025-11-15"},
        {"Control ID": "CTRL-13", "Control Name": "Management of Technical Vulnerabilities", "ISO 27001 Clause": "A.8.8", "Department": "Information Security", "Control Owner": "Alex Mercer", "Status": "Non-Compliant", "Last Review Date": "2025-06-20", "Next Review Date": "2025-12-20"},
        {"Control ID": "CTRL-14", "Control Name": "Information Security in Supplier Relationships", "ISO 27001 Clause": "A.5.19", "Department": "Legal & Procurement", "Control Owner": "Rachel Green", "Status": "Compliant", "Last Review Date": "2026-03-10", "Next Review Date": "2027-03-10"},
        {"Control ID": "CTRL-15", "Control Name": "Reporting Security Events", "ISO 27001 Clause": "A.5.24", "Department": "Information Security", "Control Owner": "Alex Mercer", "Status": "Compliant", "Last Review Date": "2026-03-25", "Next Review Date": "2027-03-25"},
        {"Control ID": "CTRL-16", "Control Name": "Incident Management and Escalation", "ISO 27001 Clause": "A.5.26", "Department": "Information Security", "Control Owner": "Alex Mercer", "Status": "Compliant", "Last Review Date": "2026-04-01", "Next Review Date": "2027-04-01"},
        {"Control ID": "CTRL-17", "Control Name": "ICT Readiness for Business Continuity", "ISO 27001 Clause": "A.5.30", "Department": "IT Operations", "Control Owner": "David Chen", "Status": "Partially Compliant", "Last Review Date": "2025-12-05", "Next Review Date": "2026-06-05"},
        {"Control ID": "CTRL-18", "Control Name": "Identification of Applicable Legislation", "ISO 27001 Clause": "A.5.36", "Department": "Legal & Procurement", "Control Owner": "Rachel Green", "Status": "Compliant", "Last Review Date": "2026-01-20", "Next Review Date": "2027-01-20"},
        {"Control ID": "CTRL-19", "Control Name": "Independent Review of InfoSec", "ISO 27001 Clause": "A.5.35", "Department": "Compliance", "Control Owner": "Sarah Jenkins", "Status": "Compliant", "Last Review Date": "2026-02-15", "Next Review Date": "2027-02-15"},
        {"Control ID": "CTRL-20", "Control Name": "Secure Coding Principles", "ISO 27001 Clause": "A.8.28", "Department": "Engineering", "Control Owner": "Marcus Vance", "Status": "Compliant", "Last Review Date": "2026-04-10", "Next Review Date": "2027-04-10"}
    ]
    pd.DataFrame(controls_data).to_csv(os.path.join(data_dir, "controls.csv"), index=False)
    
    # 2. Risk Register
    # Likelihood 1-5, Impact 1-5
    # Score = Likelihood * Impact
    # 1-5: Low, 6-10: Medium, 11-15: High, 16-25: Critical
    risks_data = [
        {"Risk ID": "RSK-01", "Risk Name": "Ransomware outbreak causing operations shutdown", "Department": "IT Operations", "Likelihood": 3, "Impact": 5, "Risk Score": 15, "Risk Level": "High", "Risk Owner": "David Chen", "Mitigation Plan": "Deploy off-site immutable backups and endpoint detection tools."},
        {"Risk ID": "RSK-02", "Risk Name": "Unauthorized privilege escalation on production servers", "Department": "Information Security", "Likelihood": 2, "Impact": 5, "Risk Score": 10, "Risk Level": "Medium", "Risk Owner": "Alex Mercer", "Mitigation Plan": "Implement Just-In-Time access controls and MFA requirements."},
        {"Risk ID": "RSK-03", "Risk Name": "Exfiltration of sensitive customer PII via unencrypted channels", "Department": "Engineering", "Likelihood": 4, "Impact": 5, "Risk Score": 20, "Risk Level": "Critical", "Risk Owner": "Marcus Vance", "Mitigation Plan": "Apply Data Loss Prevention (DLP) filters and TLS enforcement."},
        {"Risk ID": "RSK-04", "Risk Name": "Social engineering / Phishing targeting administrative staff", "Department": "HR", "Likelihood": 5, "Impact": 3, "Risk Score": 15, "Risk Level": "High", "Risk Owner": "Emma Watson", "Mitigation Plan": "Conduct quarterly phishing simulation exercises and mandatory security training."},
        {"Risk ID": "RSK-05", "Risk Name": "Vendor cloud hosting breach resulting in data exposure", "Department": "Legal & Procurement", "Likelihood": 3, "Impact": 4, "Risk Score": 12, "Risk Level": "High", "Risk Owner": "Rachel Green", "Mitigation Plan": "Enforce SOC 2 Type II audit reviews and strict vendor security clauses."},
        {"Risk ID": "RSK-06", "Risk Name": "Critical power outage in main server facility", "Department": "Facilities", "Likelihood": 1, "Impact": 4, "Risk Score": 4, "Risk Level": "Low", "Risk Owner": "John Miller", "Mitigation Plan": "Maintain dual redundant UPS backups and contract regular generator checks."},
        {"Risk ID": "RSK-07", "Risk Name": "Failure to revoke access keys for terminated employees", "Department": "HR", "Likelihood": 4, "Impact": 3, "Risk Score": 12, "Risk Level": "High", "Risk Owner": "Emma Watson", "Mitigation Plan": "Automate HR active directory sync to trigger immediate key revocations."},
        {"Risk ID": "RSK-08", "Risk Name": "Vulnerable open-source packages in internal products", "Department": "Engineering", "Likelihood": 4, "Impact": 4, "Risk Score": 16, "Risk Level": "Critical", "Risk Owner": "Marcus Vance", "Mitigation Plan": "Integrate software composition analysis (SCA) scanners into the CI/CD pipeline."},
        {"Risk ID": "RSK-09", "Risk Name": "Inadequate logging on legacy banking integrations", "Department": "Information Security", "Likelihood": 3, "Impact": 3, "Risk Score": 9, "Risk Level": "Medium", "Risk Owner": "Alex Mercer", "Mitigation Plan": "Migrate integrations to modern standard central logging frameworks."},
        {"Risk ID": "RSK-10", "Risk Name": "Non-compliance with local data protection laws (GDPR/CCPA)", "Department": "Compliance", "Likelihood": 2, "Impact": 5, "Risk Score": 10, "Risk Level": "Medium", "Risk Owner": "Sarah Jenkins", "Mitigation Plan": "Periodic legal compliance assessments and clear privacy impact analyses."},
        {"Risk ID": "RSK-11", "Risk Name": "Data leakage via physical USB drives on endpoints", "Department": "IT Operations", "Likelihood": 3, "Impact": 2, "Risk Score": 6, "Risk Level": "Medium", "Risk Owner": "David Chen", "Mitigation Plan": "Enforce USB restriction policies via Mobile Device Management (MDM)."},
        {"Risk ID": "RSK-12", "Risk Name": "Insecure third-party messaging integrations", "Department": "Compliance", "Likelihood": 3, "Impact": 3, "Risk Score": 9, "Risk Level": "Medium", "Risk Owner": "Sarah Jenkins", "Mitigation Plan": "Enforce single-sign-on (SSO) and central auditing controls on messaging integrations."}
    ]
    pd.DataFrame(risks_data).to_csv(os.path.join(data_dir, "risks.csv"), index=False)
    
    # 3. Internal Audit Findings
    # Relates to Control IDs
    audit_findings_data = [
        {
            "Finding ID": "AUD-01", 
            "Finding Title": "Missing access logs for legacy financial database", 
            "Related Control ID": "CTRL-12", 
            "Department": "Information Security", 
            "Severity": "Critical", 
            "Status": "Open", 
            "Days Open": 45, 
            "Owner": "Alex Mercer", 
            "Recommendation": "Integrate database transactions directly with the centralized SIEM logging server."
        },
        {
            "Finding ID": "AUD-02", 
            "Finding Title": "Outdated operating systems on testing environments", 
            "Related Control ID": "CTRL-13", 
            "Department": "Information Security", 
            "Severity": "High", 
            "Status": "In Progress", 
            "Days Open": 30, 
            "Owner": "Alex Mercer", 
            "Recommendation": "Update OS on all sandbox environments and incorporate them into the master patching schedule."
        },
        {
            "Finding ID": "AUD-03", 
            "Finding Title": "Delays in offboarding access permissions during employee terminations", 
            "Related Control ID": "CTRL-04", 
            "Department": "HR", 
            "Severity": "High", 
            "Status": "Overdue", 
            "Days Open": 65, 
            "Owner": "Emma Watson", 
            "Recommendation": "Implement a formal automated ticket system syncing HR departures to Active Directory."
        },
        {
            "Finding ID": "AUD-04", 
            "Finding Title": "Incomplete business continuity simulations", 
            "Related Control ID": "CTRL-17", 
            "Department": "IT Operations", 
            "Severity": "Medium", 
            "Status": "Open", 
            "Days Open": 15, 
            "Owner": "David Chen", 
            "Recommendation": "Conduct tabletop recovery exercises with key department leads and document the failover times."
        },
        {
            "Finding ID": "AUD-05", 
            "Finding Title": "Missing SSL certificates on internal administrative portals", 
            "Related Control ID": "CTRL-10", 
            "Department": "Engineering", 
            "Severity": "Medium", 
            "Status": "Closed", 
            "Days Open": 22, 
            "Owner": "Marcus Vance", 
            "Recommendation": "Deploy Let's Encrypt automated certificates to secure web consoles."
        },
        {
            "Finding ID": "AUD-06", 
            "Finding Title": "Biometric visitor check-in logs not retained", 
            "Related Control ID": "CTRL-06", 
            "Department": "Facilities", 
            "Severity": "Low", 
            "Status": "Closed", 
            "Days Open": 10, 
            "Owner": "John Miller", 
            "Recommendation": "Configure physical storage solutions to persist entry log entries for at least 90 days."
        },
        {
            "Finding ID": "AUD-07", 
            "Finding Title": "Incomplete vulnerability assessments on web applications", 
            "Related Control ID": "CTRL-13", 
            "Department": "Information Security", 
            "Severity": "High", 
            "Status": "Open", 
            "Days Open": 55, 
            "Owner": "Alex Mercer", 
            "Recommendation": "Run monthly authenticated DAST scanning reports and triage findings."
        },
        {
            "Finding ID": "AUD-08", 
            "Finding Title": "Supplier policy not updated for current remote-work standards", 
            "Related Control ID": "CTRL-14", 
            "Department": "Legal & Procurement", 
            "Severity": "Low", 
            "Status": "In Progress", 
            "Days Open": 12, 
            "Owner": "Rachel Green", 
            "Recommendation": "Draft remote-access clauses to incorporate into standard vendor service agreements."
        }
    ]
    pd.DataFrame(audit_findings_data).to_csv(os.path.join(data_dir, "audit_findings.csv"), index=False)
    
    # 4. Remediation Tracker
    # Relates to Finding IDs
    remediation_data = [
        {
            "Action ID": "REM-01", 
            "Related Finding ID": "AUD-01", 
            "Action Description": "Configure Logstash pipelines to read legacy server transaction tables.", 
            "Owner": "Alex Mercer", 
            "Due Date": "2026-06-30", 
            "Status": "In Progress", 
            "Priority": "Critical"
        },
        {
            "Action ID": "REM-02", 
            "Related Finding ID": "AUD-02", 
            "Action Description": "Retire legacy staging servers and transition code onto updated baseline instances.", 
            "Owner": "David Chen", 
            "Due Date": "2026-07-15", 
            "Status": "In Progress", 
            "Priority": "High"
        },
        {
            "Action ID": "REM-03", 
            "Related Finding ID": "AUD-03", 
            "Action Description": "Build API mapping layer connecting ADP offboarding hooks to Identity Provider.", 
            "Owner": "Emma Watson", 
            "Due Date": "2026-04-15", 
            "Status": "Overdue", 
            "Priority": "High"
        },
        {
            "Action ID": "REM-04", 
            "Related Finding ID": "AUD-04", 
            "Action Description": "Define technical business continuity targets and schedule recovery simulation calendar.", 
            "Owner": "David Chen", 
            "Due Date": "2026-08-01", 
            "Status": "Not Started", 
            "Priority": "Medium"
        },
        {
            "Action ID": "REM-05", 
            "Related Finding ID": "AUD-05", 
            "Action Description": "Install TLS certificates across network load balancers.", 
            "Owner": "Marcus Vance", 
            "Due Date": "2026-05-10", 
            "Status": "Completed", 
            "Priority": "Medium"
        },
        {
            "Action ID": "REM-06", 
            "Related Finding ID": "AUD-07", 
            "Action Description": "Configure vulnerability scanners to run weekly against production endpoints.", 
            "Owner": "Alex Mercer", 
            "Due Date": "2026-05-20", 
            "Status": "Overdue", 
            "Priority": "High"
        },
        {
            "Action ID": "REM-07", 
            "Related Finding ID": "AUD-08", 
            "Action Description": "Amend master remote-working addendum for vendor compliance reviews.", 
            "Owner": "Rachel Green", 
            "Due Date": "2026-09-01", 
            "Status": "In Progress", 
            "Priority": "Low"
        }
    ]
    pd.DataFrame(remediation_data).to_csv(os.path.join(data_dir, "remediation.csv"), index=False)
    
    # 5. Vendor Risk Module
    vendors_data = [
        {"Vendor ID": "VND-01", "Vendor Name": "Global Cloud Hosting Inc.", "Service Type": "SaaS Platform", "Department": "IT Operations", "Data Sensitivity": "High", "Risk Rating": "Critical", "Last Assessment Date": "2026-01-10", "Contract Expiry Date": "2026-12-31", "Status": "Approved"},
        {"Vendor ID": "VND-02", "Vendor Name": "SecureAuth Integrations", "Service Type": "Identity Provider", "Department": "Information Security", "Data Sensitivity": "High", "Risk Rating": "High", "Last Assessment Date": "2025-11-05", "Contract Expiry Date": "2026-06-15", "Status": "Review Required"},
        {"Vendor ID": "VND-03", "Vendor Name": "QuickComm Chat", "Service Type": "Messaging Service", "Department": "HR", "Data Sensitivity": "Medium", "Risk Rating": "Medium", "Last Assessment Date": "2026-02-20", "Contract Expiry Date": "2027-02-20", "Status": "Approved"},
        {"Vendor ID": "VND-04", "Vendor Name": "Apex Payroll Systems", "Service Type": "Financial SaaS", "Department": "HR", "Data Sensitivity": "High", "Risk Rating": "High", "Last Assessment Date": "2025-08-14", "Contract Expiry Date": "2026-08-14", "Status": "Approved"},
        {"Vendor ID": "VND-05", "Vendor Name": "Prime Dev Studio", "Service Type": "External Contractor", "Department": "Engineering", "Data Sensitivity": "Medium", "Risk Rating": "High", "Last Assessment Date": "2025-12-10", "Contract Expiry Date": "2026-05-30", "Status": "High Risk"},
        {"Vendor ID": "VND-06", "Vendor Name": "LegalForce Docs", "Service Type": "Document Management", "Department": "Legal & Procurement", "Data Sensitivity": "Medium", "Risk Rating": "Low", "Last Assessment Date": "2026-03-01", "Contract Expiry Date": "2027-03-01", "Status": "Approved"},
        {"Vendor ID": "VND-07", "Vendor Name": "OfficePower Utilities", "Service Type": "Building Operations", "Department": "Facilities", "Data Sensitivity": "Low", "Risk Rating": "Low", "Last Assessment Date": "2025-07-22", "Contract Expiry Date": "2026-07-22", "Status": "Approved"},
        {"Vendor ID": "VND-08", "Vendor Name": "ByteForce Analytics", "Service Type": "Data Storage", "Department": "Engineering", "Data Sensitivity": "High", "Risk Rating": "Critical", "Last Assessment Date": "2025-10-18", "Contract Expiry Date": "2026-04-18", "Status": "High Risk"},
        {"Vendor ID": "VND-09", "Vendor Name": "Delta Marketing CRM", "Service Type": "SaaS Platform", "Department": "Compliance", "Data Sensitivity": "High", "Risk Rating": "Medium", "Last Assessment Date": "2026-04-05", "Contract Expiry Date": "2027-04-05", "Status": "Approved"},
        {"Vendor ID": "VND-10", "Vendor Name": "EcoRecycling Hub", "Service Type": "Waste Disposal", "Department": "Facilities", "Data Sensitivity": "Low", "Risk Rating": "Low", "Last Assessment Date": "2025-09-12", "Contract Expiry Date": "2026-09-12", "Status": "Approved"}
    ]
    pd.DataFrame(vendors_data).to_csv(os.path.join(data_dir, "vendors.csv"), index=False)
    
    print("Synthetic GRC datasets successfully generated.")

if __name__ == "__main__":
    generate_synthetic_data("data")
