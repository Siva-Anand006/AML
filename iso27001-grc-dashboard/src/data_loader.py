import os
import pandas as pd
import streamlit as st
from src.data_generator import generate_synthetic_data

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

FILES = {
    "controls": "controls.csv",
    "risks": "risks.csv",
    "audit_findings": "audit_findings.csv",
    "remediation": "remediation.csv",
    "vendors": "vendors.csv"
}

def check_and_generate_data():
    """
    Checks if datasets exist. If not, generates them.
    """
    missing = False
    for filename in FILES.values():
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            missing = True
            break
            
    if missing:
        generate_synthetic_data(DATA_DIR)

def load_all_data():
    """
    Loads all GRC datasets. Initializes them in Streamlit session state if they do not exist.
    """
    check_and_generate_data()
    
    for key, filename in FILES.items():
        state_key = f"df_{key}"
        if state_key not in st.session_state:
            path = os.path.join(DATA_DIR, filename)
            st.session_state[state_key] = pd.read_csv(path)
            
    return {key: st.session_state[f"df_{key}"] for key in FILES.keys()}

def save_dataframe_to_disk(key):
    """
    Flushes a session-state dataframe to its respective CSV file on disk.
    """
    state_key = f"df_{key}"
    if state_key in st.session_state:
        path = os.path.join(DATA_DIR, FILES[key])
        st.session_state[state_key].to_csv(path, index=False)
