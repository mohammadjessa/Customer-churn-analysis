import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background-color: #0f1117;
    color: #e0e0e0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b27;
    border-right: 1px solid #2a2f3e;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #a0aec0;
    font-size: 12px;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a1f2e 0%, #1e2535 100%);
    border: 1px solid #2a3548;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
div[data-testid="metric-container"] label {
    color: #7c8fa6 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #e8eaf6 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #161b27;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #2a3548;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px;
    color: #7c8fa6;
    font-weight: 500;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
}

/* Section headers */
.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #e8eaf6;
    margin-bottom: 4px;
    padding-bottom: 8px;
    border-bottom: 2px solid #2563eb;
    display: inline-block;
}

/* Insight cards */
.insight-card {
    background: linear-gradient(135deg, #1a1f2e, #1e2535);
    border: 1px solid #2a3548;
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.insight-card.warning { border-left-color: #f59e0b; }
.insight-card.danger  { border-left-color: #ef4444; }
.insight-card.success { border-left-color: #10b981; }
.insight-card h4 { color: #e8eaf6; margin: 0 0 4px 0; font-size: 14px; font-weight: 600; }
.insight-card p  { color: #94a3b8; margin: 0; font-size: 13px; line-height: 1.5; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #1a2744 50%, #0f1117 100%);
    border: 1px solid #2a3f6f;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
}
.hero-banner h1 { color: #e8eaf6; font-size: 26px; font-weight: 700; margin: 0 0 8px 0; }
.hero-banner p  { color: #94a3b8; font-size: 14px; margin: 0; }

/* Expander */
.streamlit-expanderHeader {
    background-color: #1a1f2e !important;
    border: 1px solid #2a3548 !important;
    border-radius: 8px !important;
    color: #e8eaf6 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
DATA_URL = (
    "https://raw.githubusercontent.com/mohammadjessa/"
    "Customer-churn-analysis/main/Telco-Customer-Churn.csv"
)

@st.cache_data(show_spinner=False)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["churn"] = df["churn"].map({"Yes": 1, "No": 0})
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df["totalcharges"] = df["totalcharges"].fillna(df["totalcharges"].median())
    df["tenure_band"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0–12 months", "13–24 months", "25–48 months", "49+ months"],
        include_lowest=True,
    )
    df["charge_band"] = pd.cut(
        df["monthlycharges"],
        bins=[0, 35, 70, 100, 999],
        labels=["< $35", "$35–$70", "$70–$100", "$100+"],
        include_lowest=True,
    )
    return df

with st.spinner("Loading data..."):
    df = load_data(DATA_URL)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
FONT_CLR  = "#94a3b8"
GRID_CLR  = "#1e2535"
BLUE      = "#2563eb"
RED       = "#ef4444"
AMBER     = "#f59e0b"
GREEN     = "#10b981"

def style_fig(fig, height=340):
    fig.update_layout(
        height=height,
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        margin=dict(l=12, r=12, t=32, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color=FONT_CLR),
        xaxis=dict(gridcolor=GRID_CLR, showline=False, tickfont_color=FONT_CLR),
        yaxis=dict(gridcolor=GRID_CLR, showline=False, tickfont_color=FONT_CLR),
    )
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📡 Telco Churn Intelligence")
    st.markdown("---")
    st.markdown("**Filters**")

    contract_opts = ["All"] + sorted(df["contract"].unique().tolist())
    sel_contract  = st.selectbox("Contract Type", contract_opts)

    payment_opts  = ["All"] + sorted(df["paymentmethod"].unique().tolist())
    sel_payment   = st.selectbox("Payment Method", payment_opts)

    tenure_range  = st.slider("Tenure (months)", 0, 72, (0, 72))

    st.markdown("---")
    st.markdown("""
    **About**  
    Dataset: 7,032 telecom customers  
    Source: [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)  
    Built with Python · Plotly · Streamlit  
    """)

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_contract != "All":
    filtered = filtered[filtered["contract"] == sel_contract]
if sel_payment != "All":
    filtered = filtered[filtered["paymentmethod"] == sel_payment]
filtered = filtered[
    (filtered["tenure"] >= tenure_range[0]) &
    (filtered["tenure"] <= tenure_range[1])
]

# ── Hero banner ───────────────────────────────────────────────────────────────
churn_pct = filtered["churn"].mean() * 100
rev_at_risk = filtered[filtered["churn"] == 1]["monthlycharges"].sum()

st.markdown(f"""
<div class="hero-banner">
  <h1>📡 Telco Customer Churn Intelligence</h1>
  <p>Exploring why customers leave — and where retention efforts create the most value.<br>
  Showing <strong style="color:#e8eaf6">{len(filtered):,} customers</strong> &nbsp;·&nbsp;
  Churn rate <strong style="color:#ef4444">{churn_pct:.1f}%</strong> &nbsp;·&nbsp;
  Monthly revenue at risk <strong style="color:#f59e0b">${rev_at_risk:,.0f}</strong>
  </p>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
churned_n  = filtered["churn"].sum()
retained_n = len(filtered) - churned_n
avg_charge = filtered["monthlycharges"].mean()
avg_tenure = filtered["tenure"].mean()

c1.metric("Total Customers",       f"{len(filtered):,}")
c2.metric("Churned",               f"{churned_n:,}",  delta=f"{churn_pct:.1f}%", delta_color="inverse")
c3.metric("Avg Monthly Charge",    f"${avg_charge:.2f}")
c4.metric("Avg Tenure",            f"{avg_tenure:.0f} mo")
c5.metric("Revenue at Risk / mo",  f"${rev_at_risk:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Overview", "🔍  Deep Dive", "💡  Recommendations"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tab1:

    col_l, col_r = st.columns(2)

    # Chart 1 — Churn by Contract
    with col_l:
        st.markdown('<p class="section-title">Churn Rate by Contract Type</p>', unsafe_allow_html=True)
        contract_df = (
            df.groupby("contract")["churn"]
            .mean().mul(100).reset_index()
            .rename(columns={"churn": "churn_rate"})
            .sort_values("churn_rate", ascending=False)
        )
        fig1 = px.bar(
            contract_df, x="contract", y="churn_rate",
            color="churn_rate",
            color_continuous_scale=[[0, "#1e3a5f"], [0.5, "#2563eb"], [1, "#ef4444"]],
            text=contract_df["churn_rate"].map(lambda v: f"{v:.1f}%"),
            labels={"churn_rate": "Churn Rate (%)", "contract": ""},
        )
        fig1.update_traces(textposition="outside", textfont_color="#e8eaf6", marker_line_width=0)
        fig1.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig1), use_container_width=True)

    # Chart 2 — Churn by Payment Method
    with col_r:
        st.markdown('<p class="section-title">Churn Rate by Payment Method</p>', unsafe_allow_html=True)
        pay_df = (
            df.groupby("paymentmethod")["churn"]
            .mean().mul(100).reset_index()
            .rename(columns={"churn": "churn_rate"})
            .sort_values("churn_rate")
        )
        fig2 = px.bar(
            pay_df, x="churn_rate", y="paymentmethod",
            orientation="h",
            color="churn_rate",
            color_continuous_scale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            text=pay_df["churn_rate"].map(lambda v: f"{v:.1f}%"),
            labels={"churn_rate": "Churn Rate (%)", "paymentmethod": ""},
        )
        fig2.update_traces(textposition="outside", textfont_color="#e8eaf6", marker_line_width=0)
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig2), use_container_width=True)

    # Chart 3 — Scatter (Monthly Charges vs Tenure)
    st.markdown('<p class="section-title">Monthly Charges vs Tenure — coloured by Churn</p>', unsafe_allow_html=True)
    scatter_df = filtered.copy()
    scatter_df["Status"] = scatter_df["churn"].map({1: "Churned", 0: "Retained"})
    fig3 = px.scatter(
        scatter_df, x="tenure", y="monthlycharges",
        color="Status",
        color_discrete_map={"Churned": RED, "Retained": BLUE},
        opacity=0.55,
        labels={"tenure": "Tenure (months)", "monthlycharges": "Monthly Charges ($)"},
        hover_data={"contract": True, "paymentmethod": True},
    )
    fig3.update_traces(marker=dict(size=5))
    st.plotly_chart(style_fig(fig3, height=380), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — DEEP DIVE
# ════════════════════════════════════════════════════════════════════════════
with tab2:

    col_l, col_r = st.columns(2)

    # Chart 4 — Churn by Tenure Band
    with col_l:
        st.markdown('<p class="section-title">Churn Rate by Tenure Stage</p>', unsafe_allow_html=True)
        tenure_df = (
            df.groupby("tenure_band", observed=True)["churn"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "churn_rate", "count": "customers"})
        )
        tenure_df["churn_rate"] = tenure_df["churn_rate"] * 100
        fig4 = px.bar(
            tenure_df, x="tenure_band", y="churn_rate",
            color="churn_rate",
            color_continuous_scale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            text=tenure_df["churn_rate"].map(lambda v: f"{v:.1f}%"),
            labels={"churn_rate": "Churn Rate (%)", "tenure_band": "Tenure Stage"},
            custom_data=["customers"],
        )
        fig4.update_traces(
            textposition="outside", textfont_color="#e8eaf6",
            hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.1f}%<br>Customers: %{customdata[0]:,}<extra></extra>"
        )
        fig4.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig4), use_container_width=True)

    # Chart 5 — Churn by Monthly Charge Band
    with col_r:
        st.markdown('<p class="section-title">Churn Rate by Monthly Charge Band</p>', unsafe_allow_html=True)
        charge_df = (
            df.groupby("charge_band", observed=True)["churn"]
            .mean().mul(100).reset_index()
            .rename(columns={"churn": "churn_rate"})
        )
        fig5 = px.bar(
            charge_df, x="charge_band", y="churn_rate",
            color="churn_rate",
            color_continuous_scale=[[0, "#1e3a5f"], [0.5, "#2563eb"], [1, "#ef4444"]],
            text=charge_df["churn_rate"].map(lambda v: f"{v:.1f}%"),
            labels={"churn_rate": "Churn Rate (%)", "charge_band": "Monthly Charge"},
        )
        fig5.update_traces(textposition="outside", textfont_color="#e8eaf6", marker_line_width=0)
        fig5.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig5), use_container_width=True)

    # Chart 6 — Heatmap: Contract × Tenure Band
    st.markdown('<p class="section-title">Churn Rate Heatmap — Contract Type × Tenure Stage</p>', unsafe_allow_html=True)
    heat_df = (
        df.groupby(["contract", "tenure_band"], observed=True)["churn"]
        .mean().mul(100).reset_index()
        .rename(columns={"churn": "churn_rate"})
        .pivot(index="contract", columns="tenure_band", values="churn_rate")
    )
    fig6 = px.imshow(
        heat_df,
        color_continuous_scale=[[0, "#0d2137"], [0.4, "#2563eb"], [0.7, "#f59e0b"], [1, "#ef4444"]],
        text_auto=".1f",
        aspect="auto",
        labels={"color": "Churn %"},
    )
    fig6.update_traces(textfont_color="#ffffff")
    st.plotly_chart(style_fig(fig6, height=300), use_container_width=True)

    # Chart 7 — Box plot: Charges distribution churn vs retained
    st.markdown('<p class="section-title">Monthly Charges Distribution — Churned vs Retained</p>', unsafe_allow_html=True)
    box_df = filtered.copy()
    box_df["Status"] = box_df["churn"].map({1: "Churned", 0: "Retained"})
    fig7 = px.box(
        box_df, x="Status", y="monthlycharges",
        color="Status",
        color_discrete_map={"Churned": RED, "Retained": BLUE},
        points=False,
        labels={"monthlycharges": "Monthly Charges ($)", "Status": ""},
    )
    fig7.update_layout(showlegend=False)
    st.plotly_chart(style_fig(fig7, height=320), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown("### 📌 Key Findings")
    st.markdown("""
    <div class="insight-card danger">
        <h4>🔴 Month-to-Month Contracts are the #1 churn driver</h4>
        <p>Month-to-month customers churn at roughly 3× the rate of annual plan customers.
        The first 12 months are the highest-risk window — before loyalty and habits form.</p>
    </div>
    <div class="insight-card warning">
        <h4>🟡 Electronic Check payments signal friction, not just cost</h4>
        <p>E-check payers have the highest churn of any payment method — higher than other digital
        methods despite similar pricing. This points to friction or trust issues in that payment flow,
        not a pricing problem.</p>
    </div>
    <div class="insight-card warning">
        <h4>🟡 High charges + short tenure = highest-risk customer profile</h4>
        <p>Customers paying $70–$100+/month in their first year are the riskiest segment.
        They're paying full price without having built loyalty or integrated the service into their routine.</p>
    </div>
    <div class="insight-card success">
        <h4>🟢 Long-tenure customers are highly stable</h4>
        <p>Customers past the 48-month mark churn at under 8% regardless of contract type.
        Loyalty programmes that push customers to this milestone deliver outsized retention value.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Business Recommendations")
    rec_l, rec_r = st.columns(2)

    with rec_l:
        st.markdown("""
        <div class="insight-card">
            <h4>1. Incentivise early contract upgrades</h4>
            <p>Target month-to-month customers in months 1–6 with a modest discount on a 12-month
            plan. The churn savings more than offset the discount cost. Even a $5/month reduction
            to lock in a year recovers well within the average customer lifetime.</p>
        </div>
        <div class="insight-card">
            <h4>2. Audit the electronic check payment flow</h4>
            <p>Run a UX audit specifically on the e-check journey — payment failure rates, load times,
            and trust signals. Migrating even 20% of e-check users to auto-pay would meaningfully
            reduce churn in that segment.</p>
        </div>
        """, unsafe_allow_html=True)

    with rec_r:
        st.markdown("""
        <div class="insight-card">
            <h4>3. Build a high-risk CRM flag</h4>
            <p>The SQL already defines a <code>risk_segment</code> field. Pipe that into a lifecycle
            email tool for targeted outreach: contract upgrade offer, onboarding check-in at month 3,
            and a loyalty milestone reward at month 12.</p>
        </div>
        <div class="insight-card">
            <h4>4. Protect the high-charge, short-tenure cohort</h4>
            <p>Customers paying $70+/month in year 1 represent the highest revenue-at-risk group.
            A dedicated onboarding programme (personalised support, usage tips, check-in calls)
            for this cohort is the highest-ROI intervention available.</p>
        </div>
        """, unsafe_allow_html=True)

    # Revenue at risk summary
    st.markdown("### 💰 Revenue at Risk Summary")
    risk_df = (
        df[df["churn"] == 1]
        .groupby("contract")
        .agg(
            customers=("churn", "count"),
            monthly_rev_at_risk=("monthlycharges", "sum"),
            avg_charge=("monthlycharges", "mean"),
        )
        .reset_index()
        .sort_values("monthly_rev_at_risk", ascending=False)
    )
    risk_df["monthly_rev_at_risk"] = risk_df["monthly_rev_at_risk"].map("${:,.0f}".format)
    risk_df["avg_charge"]          = risk_df["avg_charge"].map("${:.2f}".format)
    risk_df.columns                = ["Contract Type", "Churned Customers", "Monthly Revenue at Risk", "Avg Monthly Charge"]
    st.dataframe(risk_df, use_container_width=True, hide_index=True)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("🗂  View raw data"):
    st.dataframe(
        filtered.drop(columns=["tenure_band", "charge_band"], errors="ignore")
        .reset_index(drop=True),
        use_container_width=True,
        height=300,
    )

