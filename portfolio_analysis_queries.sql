-- ============================================================
-- Telco Customer Churn — Portfolio Analysis Queries
-- Dialect: BigQuery Standard SQL
-- Source table: customer_churn_clean  (see customer_churn_clean_bigquery.sql)
-- Replace your_project.your_dataset with your actual project/dataset
-- ============================================================


-- ── 1. Risk segment rollup ────────────────────────────────────────────────────
-- Summarises churn rate and monthly revenue at risk by pre-built risk tier.
-- Useful as a top-level executive view or dashboard KPI card.

SELECT
    risk_segment,
    COUNT(DISTINCT customer_id)                             AS customers,
    SUM(churn_flag)                                         AS churned,
    ROUND(SAFE_DIVIDE(SUM(churn_flag), COUNT(*)), 4)        AS churn_rate,
    ROUND(SUM(IF(churn_flag = 1, monthly_charges, 0)), 2)   AS monthly_revenue_at_risk
FROM `your_project.your_dataset.customer_churn_clean`
GROUP BY risk_segment
ORDER BY
    CASE risk_segment
        WHEN 'Critical' THEN 1
        WHEN 'High'     THEN 2
        WHEN 'Moderate' THEN 3
        ELSE 4
    END;


-- ── 2. High-impact churn segments ranked by revenue at risk ───────────────────
-- Cross-cuts contract, internet service, payment method, and support profile.
-- Filtered to segments with 100+ customers to avoid noise from tiny groups.
-- revenue_risk_rank tells you where to focus retention spend first.

WITH segment_summary AS (
    SELECT
        contract,
        internet_service,
        payment_method,
        payment_mode,
        support_profile,
        COUNT(DISTINCT customer_id)                             AS customers,
        SUM(churn_flag)                                         AS churned,
        ROUND(SAFE_DIVIDE(SUM(churn_flag), COUNT(*)), 4)        AS churn_rate,
        ROUND(SUM(IF(churn_flag = 1, monthly_charges, 0)), 2)   AS monthly_revenue_at_risk
    FROM `your_project.your_dataset.customer_churn_clean`
    GROUP BY 1, 2, 3, 4, 5
)

SELECT
    *,
    DENSE_RANK() OVER (ORDER BY monthly_revenue_at_risk DESC) AS revenue_risk_rank,
    DENSE_RANK() OVER (ORDER BY churn_rate DESC)              AS churn_rate_rank
FROM segment_summary
WHERE customers >= 100
ORDER BY monthly_revenue_at_risk DESC, churn_rate DESC;


-- ── 3. Retention lever comparison — billing and support ───────────────────────
-- Stacks payment mode and support profile in one result so you can compare
-- which levers are associated with lower churn without running separate queries.

WITH lever_rollup AS (

    SELECT
        'Payment mode'  AS lever_type,
        payment_mode    AS lever_value,
        COUNT(*)        AS customers,
        ROUND(SAFE_DIVIDE(SUM(churn_flag), COUNT(*)), 4)  AS churn_rate,
        ROUND(AVG(monthly_charges), 2)                    AS avg_monthly_charge
    FROM `your_project.your_dataset.customer_churn_clean`
    GROUP BY 1, 2

    UNION ALL

    SELECT
        'Support profile'   AS lever_type,
        support_profile     AS lever_value,
        COUNT(*)            AS customers,
        ROUND(SAFE_DIVIDE(SUM(churn_flag), COUNT(*)), 4)  AS churn_rate,
        ROUND(AVG(monthly_charges), 2)                    AS avg_monthly_charge
    FROM `your_project.your_dataset.customer_churn_clean`
    GROUP BY 1, 2

)

SELECT
    lever_type,
    lever_value,
    customers,
    churn_rate,
    avg_monthly_charge
FROM lever_rollup
ORDER BY lever_type, churn_rate DESC;


-- ── 4. tenure_months bucket breakdown ────────────────────────────────────────────────
-- Groups customers into cohorts by how long they've been a customer.
-- Early-tenure_months customers (0–12 months) on month-to-month contracts
-- are consistently the highest-risk group — this query surfaces that clearly.

SELECT
    CASE
        WHEN tenure_months BETWEEN 0  AND 12 THEN '0–12 months'
        WHEN tenure_months BETWEEN 13 AND 24 THEN '13–24 months'
        WHEN tenure_months BETWEEN 25 AND 48 THEN '25–48 months'
        ELSE '49+ months'
    END                                                     AS tenure_months_bucket,
    contract,
    COUNT(*)                                                AS customers,
    ROUND(SAFE_DIVIDE(SUM(churn_flag), COUNT(*)), 4)        AS churn_rate,
    ROUND(AVG(monthly_charges), 2)                          AS avg_monthly_charge
FROM `your_project.your_dataset.customer_churn_clean`
GROUP BY 1, 2
ORDER BY
    CASE tenure_months_bucket
        WHEN '0–12 months'  THEN 1
        WHEN '13–24 months' THEN 2
        WHEN '25–48 months' THEN 3
        ELSE 4
    END,
    churn_rate DESC;
