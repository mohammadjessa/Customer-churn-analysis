import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn Dashboard",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Telco Customer Churn Analysis")
st.markdown("Exploring what drives customer churn — and where retention efforts should focus.")
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
DATA_URL = (
    "https://raw.githubusercontent.com/mohammadjessa/"
    "Customer-churn-analysis/main/Telco-Customer-Churn.csv"
)

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["churn"] = df["churn"].map({"Yes": 1, "No": 0})
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df["totalcharges"].fillna(df["totalcharges"].median(), inplace=True)
    return df

df = load_data(DATA_URL)

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")

contract_options = ["All"] + sorted(df["contract"].unique().tolist())
selected_contract = st.sidebar.selectbox("Contract Type", contract_options)

payment_options = ["All"] + sorted(df["paymentmethod"].unique().tolist())
selected_payment = st.sidebar.selectbox("Payment Method", payment_options)

filtered = df.copy()
if selected_contract != "All":
    filtered = filtered[filtered["contract"] == selected_contract]
if selected_payment != "All":
    filtered = filtered[filtered["paymentmethod"] == selected_payment]

# ── Top metrics ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Customers", f"{len(filtered):,}")
with col2:
    churn_rate = filtered["churn"].mean() * 100
    st.metric("Churn Rate", f"{churn_rate:.1f}%")
with col3:
    avg_charge = filtered["monthlycharges"].mean()
    st.metric("Avg Monthly Charge", f"${avg_charge:.2f}")
with col4:
    avg_tenure = filtered["tenure"].mean()
    st.metric("Avg Tenure (months)", f"{avg_tenure:.0f}")

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Churn Rate by Contract Type")
    contract_churn = (
        df.groupby("contract")["churn"]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={"churn": "churn_rate"})
        .sort_values("churn_rate", ascending=False)
    )
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=contract_churn, x="contract", y="churn_rate", palette="Reds_r", ax=ax1)
    ax1.set_xlabel("Contract Type")
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_title("")
    for bar in ax1.patches:
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{bar.get_height():.1f}%",
            ha="center", va="bottom", fontsize=10
        )
    sns.despine()
    st.pyplot(fig1)

with col_right:
    st.subheader("Churn Rate by Payment Method")
    pay_churn = (
        df.groupby("paymentmethod")["churn"]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={"churn": "churn_rate"})
        .sort_values("churn_rate", ascending=False)
    )
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=pay_churn, x="churn_rate", y="paymentmethod", palette="Blues_r", ax=ax2)
    ax2.set_xlabel("Churn Rate (%)")
    ax2.set_ylabel("")
    ax2.set_title("")
    sns.despine()
    st.pyplot(fig2)

st.divider()

# ── Scatter: Monthly charges vs tenure ───────────────────────────────────────
st.subheader("Monthly Charges vs Tenure — coloured by Churn")

fig3, ax3 = plt.subplots(figsize=(10, 4))
colors = filtered["churn"].map({1: "#e63946", 0: "#457b9d"})
ax3.scatter(
    filtered["tenure"],
    filtered["monthlycharges"],
    c=colors,
    alpha=0.4,
    s=12
)
ax3.set_xlabel("Tenure (months)")
ax3.set_ylabel("Monthly Charges ($)")
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#e63946", label="Churned"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#457b9d", label="Retained"),
]
ax3.legend(handles=legend_elements)
sns.despine()
st.pyplot(fig3)

st.divider()

# ── Raw data ──────────────────────────────────────────────────────────────────
with st.expander("View raw data"):
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
