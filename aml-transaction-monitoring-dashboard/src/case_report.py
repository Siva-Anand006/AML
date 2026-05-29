def generate_case_summary(row) -> str:
    """
    Generates an investigation-ready narrative report based on transaction features
    and triggered rules. Ideal for copy-pasting into internal case notes.
    """
    triggered_rules = []

    rule_descriptions = {
        "rule_high_value": "high-value transaction",
        "rule_unusual_amount": "transaction amount significantly above customer average",
        "rule_high_velocity": "high transaction velocity",
        "rule_structuring": "possible structuring below reporting threshold",
        "rule_high_total_sender_value": "high total sender transaction value",
        "rule_high_risk_country": "connection to high-risk geography",
    }

    # Identify all rules triggered in this transaction row
    for rule, description in rule_descriptions.items():
        if rule in row and bool(row[rule]):
            triggered_rules.append(description)

    rules_text = ", ".join(triggered_rules) if triggered_rules else "no major rule triggers"

    return (
        f"Customer/account {row.get('sender', 'Unknown')} initiated a transaction of "
        f"{row.get('amount', 0):,.2f} to {row.get('receiver', 'Unknown')}. "
        f"The transaction was assigned a risk score of {row.get('risk_score', 0)} "
        f"and classified as {row.get('risk_level', 'Unknown')} risk. "
        f"Triggered indicators include: {rules_text}. "
        f"Recommended action: review customer profile, transaction history, source of funds, "
        f"and determine whether escalation is required."
    )
