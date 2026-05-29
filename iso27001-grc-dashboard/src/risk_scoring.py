def calculate_risk_score(likelihood, impact):
    """
    Computes standard risk score as Likelihood multiplied by Impact.
    """
    try:
        return int(likelihood) * int(impact)
    except (ValueError, TypeError):
        return 0

def determine_risk_level(score):
    """
    Categorizes risk score into ISO 27001 regulatory risk levels.
    """
    if score <= 5:
        return "Low"
    elif score <= 10:
        return "Medium"
    elif score <= 15:
        return "High"
    else:
        return "Critical"

def get_risk_color(level):
    """
    Returns hex codes for compliance risk severity colors.
    """
    colors = {
        "Low": "#059669",      # Emerald Green
        "Medium": "#D97706",   # Amber Gold
        "High": "#EA580C",     # Orange-Red
        "Critical": "#DC2626"  # Crimson Red
    }
    return colors.get(level, "#6B7280")
