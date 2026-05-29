import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_aml_data(output_path: str, num_rows: int = 15000):
    """
    Generates a high-fidelity synthetic AML transaction dataset matching the SAML-D schema.
    Injects specific money laundering typologies (structuring, velocity, country risk, amount spikes).
    """
    np.random.seed(42)
    random.seed(42)

    # Base parameters
    start_date = datetime(2026, 1, 1)
    payment_types = ["ACH", "Wire", "Credit Card", "Debit Card", "Cheque", "Cash Transfer"]
    currencies = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]
    
    countries_normal = [
        "United States", "United Kingdom", "Germany", "France", "Canada", 
        "Australia", "Japan", "Singapore", "Switzerland", "Brazil", "India"
    ]
    countries_high_risk = ["Iran", "North Korea", "Syria", "Russia", "Myanmar", "Afghanistan"]

    print(f"Generating {num_rows} synthetic transactions mimicking SAML-D schema...")

    # Pre-generate accounts
    senders = [f"ACC-S{i:05d}" for i in range(1, 2001)]
    receivers = [f"ACC-R{i:05d}" for i in range(1, 2001)]
    
    # Pre-assign sender base characteristics (to maintain consistency)
    sender_country_map = {acc: random.choice(countries_normal) for acc in senders}
    sender_avg_amt_map = {acc: random.uniform(50, 1500) for acc in senders}
    
    data = []

    # Helper to create a single transaction record
    def create_record(step, date_val, sender, receiver, amount, p_type, sender_country, receiver_country, is_laundering=0):
        # Time step as simulated hours/seconds
        time_str = (date_val + timedelta(seconds=random.randint(0, 86399))).strftime("%H:%M:%S")
        date_str = date_val.strftime("%Y-%m-%d")
        
        p_curr = random.choice(currencies)
        # 90% chance received currency matches, 10% foreign exchange
        r_curr = p_curr if random.random() < 0.90 else random.choice(currencies)
        
        return {
            "Time": time_str,
            "Date": date_str,
            "Sender_account": sender,
            "Receiver_account": receiver,
            "Amount": round(amount, 2),
            "Payment_currency": p_curr,
            "Received_currency": r_curr,
            "Sender_bank_location": sender_country,
            "Receiver_bank_location": receiver_country,
            "Payment_type": p_type,
            "Is_laundering": is_laundering
        }

    # 1. Generate standard normal transactions (about 90% of data)
    normal_rows = int(num_rows * 0.90)
    current_date = start_date
    for i in range(normal_rows):
        if i % 500 == 0:
            current_date += timedelta(days=1)
            
        sender = random.choice(senders)
        receiver = random.choice(receivers)
        
        # Lognormal distribution for transaction amounts (mostly small, rare larger ones)
        base_avg = sender_avg_amt_map[sender]
        amount = np.random.lognormal(mean=np.log(base_avg), sigma=0.5)
        amount = min(amount, 15000.0) # Cap normal transactions
        
        sender_country = sender_country_map[sender]
        receiver_country = random.choice(countries_normal)
        p_type = random.choice(payment_types)
        
        data.append(create_record(i, current_date, sender, receiver, amount, p_type, sender_country, receiver_country, 0))

    # 2. Inject AML Typology A: Structuring / Smurfing (just below reporting limit of $10,000)
    # We create specific malicious senders performing multiple transactions in the range $9,000 to $9,990
    print("Injecting Structuring typologies...")
    structuring_senders = [f"BAD-STR{i:03d}" for i in range(1, 15)]
    structuring_receivers = [f"REC-STR{i:03d}" for i in range(1, 15)]
    
    for idx, sender in enumerate(structuring_senders):
        receiver = structuring_receivers[idx]
        sender_country = "United States"
        receiver_country = "Canada"
        
        # Each sender performs 4-7 transactions of amounts between $9,000 and $9,980
        num_txns = random.randint(4, 7)
        for t in range(num_txns):
            txn_date = start_date + timedelta(days=random.randint(1, 25))
            amount = random.uniform(9000.0, 9990.0)
            p_type = "Cash Transfer" if random.random() < 0.6 else "Wire"
            data.append(create_record(len(data), txn_date, sender, receiver, amount, p_type, sender_country, receiver_country, 1))

    # 3. Inject AML Typology B: High Velocity (rapid sequence of transactions)
    print("Injecting High Velocity typologies...")
    velocity_senders = [f"BAD-VEL{i:03d}" for i in range(1, 15)]
    for sender in velocity_senders:
        receiver = random.choice(receivers)
        sender_country = random.choice(countries_normal)
        receiver_country = random.choice(countries_normal)
        
        # Senders making 12-20 transactions within a single day
        txn_date = start_date + timedelta(days=random.randint(5, 25))
        num_txns = random.randint(12, 20)
        for t in range(num_txns):
            amount = random.uniform(100.0, 4000.0)
            p_type = "Wire"
            data.append(create_record(len(data), txn_date, sender, receiver, amount, p_type, sender_country, receiver_country, 1))

    # 4. Inject AML Typology C: High-Risk Geographies
    print("Injecting High-Risk Geography typologies...")
    geo_senders = [f"BAD-GEO{i:03d}" for i in range(1, 20)]
    for sender in geo_senders:
        receiver = random.choice(receivers)
        sender_country = random.choice(countries_high_risk)
        receiver_country = random.choice(countries_normal)
        
        # 2-4 transactions per sender
        num_txns = random.randint(2, 4)
        for t in range(num_txns):
            txn_date = start_date + timedelta(days=random.randint(2, 28))
            amount = random.uniform(500.0, 15000.0)
            p_type = "Wire"
            data.append(create_record(len(data), txn_date, sender, receiver, amount, p_type, sender_country, receiver_country, 1))

    # 5. Inject AML Typology D: Unusual Customer Amount Spikes (3x-5x their average)
    print("Injecting Unusual Amount Spikes typologies...")
    spike_senders = random.sample(senders, 40)
    for sender in spike_senders:
        # First, add a couple of normal small transactions to establish history
        sender_country = sender_country_map[sender]
        receiver = random.choice(receivers)
        receiver_country = random.choice(countries_normal)
        
        # Establish low average history
        history_avg = 100.0
        for _ in range(3):
            txn_date = start_date + timedelta(days=random.randint(1, 10))
            amount = random.uniform(50.0, 150.0)
            data.append(create_record(len(data), txn_date, sender, receiver, amount, "Debit Card", sender_country, receiver_country, 0))
            
        # Injected spike transaction (significantly above typical average)
        txn_date = start_date + timedelta(days=random.randint(12, 28))
        amount = history_avg * random.uniform(4.5, 8.0)  # 450 - 800
        p_type = "Wire"
        data.append(create_record(len(data), txn_date, sender, receiver, amount, p_type, sender_country, receiver_country, 1))

    # 6. Inject AML Typology E: Massive High-Value Transactions
    print("Injecting Massive High-Value typologies...")
    whale_senders = [f"BAD-WHL{i:03d}" for i in range(1, 10)]
    for sender in whale_senders:
        receiver = random.choice(receivers)
        sender_country = random.choice(countries_normal)
        receiver_country = random.choice(countries_normal)
        
        # Giant transactions >= 99th percentile of typical data
        txn_date = start_date + timedelta(days=random.randint(1, 28))
        amount = random.uniform(150000.0, 450000.0)
        p_type = "Wire"
        data.append(create_record(len(data), txn_date, sender, receiver, amount, p_type, sender_country, receiver_country, 1))

    # Compile and shuffle so it looks like an actual transaction stream
    df = pd.DataFrame(data)
    
    # Convert Time & Date to sort chronologically
    df["datetime_sort"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df = df.sort_values("datetime_sort").reset_index(drop=True)
    df = df.drop(columns=["datetime_sort"])
    
    # Save to disk
    df.to_csv(output_path, index=False)
    print(f"Successfully generated synthetic dataset with {len(df)} rows saved to {output_path}!")
    print(f"Suspicious alerting rates: {df['Is_laundering'].mean() * 100:.2f}% (Total alerts: {df['Is_laundering'].sum()})")

if __name__ == "__main__":
    import sys
    path = "data/aml_transactions.csv"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    generate_synthetic_aml_data(path)
