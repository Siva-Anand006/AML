import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """
    Load AML transaction dataset.
    Normalizes column headers to snake_case.
    """
    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create standardized columns used by the Streamlit app.
    Ensures compatibility with multiple dataset versions, including raw SAML-D.
    """
    column_map_candidates = {
        "amount": ["amount", "transaction_amount", "payment_amount"],
        "sender": ["sender", "nameorig", "account_from", "from_account", "sender_account"],
        "receiver": ["receiver", "namedest", "account_to", "to_account", "receiver_account"],
        "transaction_type": ["type", "transaction_type", "payment_type"],
        "timestamp": ["timestamp", "date", "datetime", "step"],
        "is_laundering": ["is_laundering", "isfraud", "laundering", "is_suspicious", "label"],
        "sender_country": ["sender_country", "origin_country", "country_from", "sender_bank_location"],
        "receiver_country": ["receiver_country", "destination_country", "country_to", "receiver_bank_location"],
    }

    for standard_col, possible_cols in column_map_candidates.items():
        if standard_col not in df.columns:
            for col in possible_cols:
                if col in df.columns:
                    df[standard_col] = df[col]
                    break

    if "amount" not in df.columns:
        raise ValueError("No amount column found. Check your dataset column names.")

    if "sender" not in df.columns:
        df["sender"] = "UNKNOWN_SENDER_" + df.index.astype(str)

    if "receiver" not in df.columns:
        df["receiver"] = "UNKNOWN_RECEIVER_" + df.index.astype(str)

    if "transaction_type" not in df.columns:
        df["transaction_type"] = "UNKNOWN"

    if "timestamp" not in df.columns:
        df["timestamp"] = df.index

    if "is_laundering" not in df.columns:
        df["is_laundering"] = 0

    if "sender_country" not in df.columns:
        df["sender_country"] = "Unknown"

    if "receiver_country" not in df.columns:
        df["receiver_country"] = "Unknown"

    # Standardize types and clean numeric amounts
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["is_laundering"] = pd.to_numeric(df["is_laundering"], errors="coerce").fillna(0).astype(int)

    return df
