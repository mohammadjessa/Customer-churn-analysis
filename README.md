# Telco Customer Churn Analysis

An end-to-end data analysis project exploring why telecom customers leave — and what the business can do about it.

The dataset covers 7,032 customers with features including contract type, payment method, monthly charges, tenure, and service usage. The goal was to go beyond surface-level churn rates and pinpoint where the business is losing the most revenue.

---

## Key Findings

- **Overall churn rate: 26.6%**
- Month-to-month contract customers churn at roughly **3× the rate** of those on annual or two-year plans
- **Electronic check** payers have the highest churn of any payment method — points to friction rather than a pricing issue
- High monthly charges combined with short tenure is the highest-risk combination — these customers haven't built loyalty yet and are paying full price

---

## Project Structure

```
Customer-churn-analysis/
├── telco-customer-churn.ipynb          # Main analysis — EDA, visualisations, feature breakdown
├── app.py                              # Streamlit dashboard
├── portfolio_analysis_queries.sql      # BigQuery: segment rollups, revenue at risk, retention levers
├── customer_churn_clean_bigquery.sql   # Data cleaning script for BigQuery
├── requirements.txt                    # Python dependencies
└── telco_customer_churn_dashboard_preview.pdf  # Looker Studio dashboard export
```

**Dataset:** [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## Quickstart

**Streamlit app**
## 🚀 Live Demo
👉 [Open Streamlit Dashboard](https://customer-churn-analysis-farmmh8hysewfyckrgpycy.streamlit.app/)

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app pulls the CSV directly from this repo — no local file needed.

**SQL (BigQuery)**

Run `customer_churn_clean_bigquery.sql` first to create the `customer_churn_clean` table, then run the queries in `portfolio_analysis_queries.sql`. Replace `your_project.your_dataset` with your own path.

---

## Business Recommendations

**1. Incentivise longer contracts early**

The data supports targeting month-to-month customers in their first 6 months — that's when the churn risk is highest and before habits form. Even a modest discount on a 12-month plan likely pays for itself.

**2. Investigate the electronic check payment flow**

E-check churn is higher than other digital payment methods, which suggests friction or trust issues rather than cost. Worth auditing that specific flow.

**3. Build a high-risk segment flag for the CRM**

The SQL already defines a `risk_segment` field based on contract type, tenure, and charge level. Piping that into a lifecycle email tool is a low-lift next step with clear targeting logic.

---

## Tools

| Tool | Use |
|---|---|
| Python · Pandas | Data cleaning and analysis |
| Matplotlib · Seaborn | Visualisations |
| Jupyter Notebook | Exploratory analysis |
| Streamlit | Interactive dashboard |
| BigQuery SQL | Segmentation and revenue analysis |
| Looker Studio | Dashboard (PDF export included) |
