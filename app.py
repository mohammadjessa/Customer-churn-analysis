import streamlit as st
import pandas as pd

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(page_title="Churn Dashboard", layout="wide")
st.title("📊 Customer Churn Dashboard")

# =============================================
# LOAD DATA FROM GITHUB
# =============================================
url = "https://raw.githubusercontent.com/mohammadjessa/Customer-churn-analysis/main/Telco-Customer-Churn.csv"

df = pd.read_csv(url)

# =============================================
# CLEAN DATA
# =============================================
df.columns = df.columns.str.strip().str.lower()

# Convert churn to numeric (FIXES YOUR ERROR)
df['churn'] = df['churn'].map({'Yes': 1, 'No': 0})

# Convert totalcharges properly
df['totalcharges'] = pd.to_numeric(df['totalcharges'], errors='coerce')
df['totalcharges'].fillna(df['totalcharges'].median(), inplace=True)

# =============================================
# PREVIEW
# =============================================
st.subheader("Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# =============================================
# METRICS
# =============================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", len(df))

with col2:
    churn_rate = df['churn'].mean() * 100
    st.metric("Churn Rate", f"{churn_rate:.1f}%")

with col3:
    avg_charge = df['monthlycharges'].mean()
    st.metric("Avg Monthly Charge", f"${avg_charge:.2f}")
