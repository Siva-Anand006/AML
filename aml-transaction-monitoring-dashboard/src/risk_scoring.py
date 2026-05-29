import pandas as pd

def calculate_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates weighted AML risk score (0-100) based on triggered rules.
    Categorizes risk level into Low, Medium, High, or Critical.
    Sets alert flag for transactions scoring 50 or above.
    """
    df = df.copy()

    df["risk_score"] = 0

    # Weighted scoring mechanism
    scoring_rules = {
        "rule_high_value": 25,
        "rule_unusual_amount": 20,
        "rule_high_velocity": 20,
        "rule_structuring": 25,
        "rule_high_total_sender_value": 15,
        "rule_high_risk_country": 30,
    }

    # Sum points from triggered rules
    for rule, points in scoring_rules.items():
        if rule in df.columns:
            df["risk_score"] += df[rule].astype(int) * points

    # Clip scores to ensure they do not exceed 100
    df["risk_score"] = df["risk_score"].clip(0, 100)

    # Risk level classification
    if len(df) == 0:
        df["risk_level"] = pd.Series([], dtype="category")
        df["is_alert"] = pd.Series([], dtype=bool)
    else:
        df["risk_level"] = pd.cut(
            df["risk_score"],
            bins=[-1, 24, 49, 74, 100],
            labels=["Low", "Medium", "High", "Critical"]
        )
        df["is_alert"] = df["risk_score"] >= 50

    return df
