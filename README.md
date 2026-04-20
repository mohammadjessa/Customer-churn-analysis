Telco Customer Churn Analysis
An end-to-end data analysis project exploring why telecom customers leave — and what the business can do about it.
The dataset covers 7,032 customers and includes contract type, payment method, monthly charges, tenure, and service usage. The goal was to move beyond surface-level churn rates and actually pinpoint where the business is losing the most revenue.
***What I Found
Overall churn rate: 26.6% — higher than the industry average, which made the contract type breakdown the most interesting part of this analysis
Customers on month-to-month contracts churn at roughly 3x the rate of those on annual or two-year plans — the drop-off is steep and consistent across charge levels
Electronic check payers have the highest churn of any payment method, which points to a friction or trust issue rather than a pricing one
High monthly charges alone don't explain churn, but high charges combined with short tenure is where the real concentration is — those customers haven't had time to build loyalty and are paying full price
***Files in This Repo
File	What it does
`telco-customer-churn.ipynb`	Main analysis notebook — EDA, visualizations, feature breakdown
`app.py`	Streamlit dashboard for interactive exploration
`portfolio_analysis_queries.sql`	BigQuery SQL: segment rollups, revenue at risk, retention lever analysis
`customer_churn_clean_bigquery.sql`	Data cleaning logic prepared for BigQuery
`requirements.txt`	Python dependencies
`telco_customer_churn_dashboard_preview.pdf`	Screenshot/export of the Looker Studio dashboard
Dataset: Telco Customer Churn on Kaggle
***Running the Streamlit App
pip install -r requirements.txt
streamlit run app.py
The app loads the data directly from this repo, so no local CSV needed.
***Running the SQL
The SQL files are written for BigQuery. Replace your_project.your_dataset with your own project/dataset path. The cleaning script (customer_churn_clean_bigquery.sql) should be run first — it outputs the customer_churn_clean table that the analysis queries depend on.
***Business Recommendations
1. Push month-to-month customers toward annual contracts
A discount of even 10–15% on a 12-month commitment would likely pay for itself given the churn differential. The data supports targeting customers in months 2–6 of tenure, before habits form.
2. Look at the electronic check experience specifically
The churn rate for e-check users is noticeably higher than other payment methods, including other digital ones. This doesn't look like a price problem — it's worth checking whether that payment flow has friction, failures, or trust issues.
3. Build a high-risk segment flag
The SQL in portfolio_analysis_queries.sql already defines a risk_segment field. Piping that into a CRM or lifecycle email tool is a straightforward next step — the segments are defined by contract type, tenure bucket, and charge level.
***Tools Used
Python (Pandas, Matplotlib, Seaborn)
Jupyter Notebook
Streamlit
BigQuery SQL
Looker Studio (dashboard export in PDF)
