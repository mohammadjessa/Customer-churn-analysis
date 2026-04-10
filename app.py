import streamlit as st
import pandas as pd

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(page_title="Churn Dashboard", layout="wide")
st.title("📊 Customer Churn Dashboard")

# =============================================
# FILE UPLOAD
# =============================================
uploaded = st.file_uploader("Upload your churn CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # =============================================
    # METRICS
    # =============================================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Customers", len(df))

    with col2:
        # Handle both Yes/No and 0/1
        if df['churn'].dtype == 'object':
            churn_rate = df['churn'].value_counts(normalize=True).get('Yes', 0) * 100
        else:
            churn_rate = df['churn'].mean() * 100

        st.metric("Churn Rate", f"{churn_rate:.1f}%")

    with col3:
        avg_charge = df['monthlycharges'].mean()
        st.metric("Avg Monthly Charge", f"${avg_charge:.2f}")
