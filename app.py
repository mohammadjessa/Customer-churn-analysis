import streamlit as st
import pandas as pd

st.set_page_config(page_title="Churn Dashboard", layout="wide")
st.title("📊 Customer Churn Dashboard")

uploaded = st.file_uploader("Upload your churn CSV", type= )
if uploaded:
    df = pd.read_csv(uploaded)
    st.dataframe(df.head(), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", len(df))
    with col2:
        churn_rate = (df .value_counts(normalize=True).get('Yes', 0) * 100)
        st.metric("Churn Rate", f"{churn_rate:.1f}%")
    with col3:
        st.metric("Avg Monthly Charge", f"${df .mean():.0f}")
    
    st.write("Your charts and full analysis will show here once you add them.")
