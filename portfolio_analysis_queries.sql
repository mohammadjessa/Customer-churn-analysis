-- Query 1: Risk segment rollup for retention prioritization
SELECT
  risk_segment,
  COUNT(DISTINCT customer_id) AS customers,
  SUM(churn_flag) AS churned_customers,
  SAFE_DIVIDE(SUM(churn_flag), COUNT(*)) AS churn_rate,
  SUM(IF(churn_flag = 1, monthly_charges, 0)) AS monthly_revenue_at_risk
FROM `your_project.your_dataset.customer_churn_clean`
GROUP BY 1
ORDER BY
  CASE risk_segment
    WHEN 'Critical' THEN 1
    WHEN 'High' THEN 2
    WHEN 'Moderate' THEN 3
    ELSE 4
  END;

-- Query 2: High-impact churn segments ranked by revenue at risk
WITH segment_summary AS (
  SELECT
    contract,
    internet_service,
    payment_method,
    payment_mode,
    support_profile,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(churn_flag) AS churned_customers,
    SAFE_DIVIDE(SUM(churn_flag), COUNT(*)) AS churn_rate,
    SUM(IF(churn_flag = 1, monthly_charges, 0)) AS monthly_revenue_at_risk
  FROM `your_project.your_dataset.customer_churn_clean`
  GROUP BY 1, 2, 3, 4, 5
)
SELECT
  *,
  DENSE_RANK() OVER (ORDER BY monthly_revenue_at_risk DESC) AS revenue_risk_rank,
  DENSE_RANK() OVER (ORDER BY churn_rate DESC) AS churn_rank
FROM segment_summary
WHERE customers >= 100
ORDER BY monthly_revenue_at_risk DESC, churn_rate DESC;

-- Query 3: Retention lever comparison for billing and support
WITH lever_rollup AS (
  SELECT
    'Payment mode' AS lever_type,
    payment_mode AS lever_group,
    COUNT(*) AS customers,
    SAFE_DIVIDE(SUM(churn_flag), COUNT(*)) AS churn_rate,
    AVG(monthly_charges) AS avg_monthly_charges
  FROM `your_project.your_dataset.customer_churn_clean`
  GROUP BY 1, 2

  UNION ALL

  SELECT
    'Support profile' AS lever_type,
    support_profile AS lever_group,
    COUNT(*) AS customers,
    SAFE_DIVIDE(SUM(churn_flag), COUNT(*)) AS churn_rate,
    AVG(monthly_charges) AS avg_monthly_charges
  FROM `your_project.your_dataset.customer_churn_clean`
  GROUP BY 1, 2
)
SELECT
  lever_type,
  lever_group,
  customers,
  churn_rate,
  avg_monthly_charges
FROM lever_rollup
ORDER BY lever_type, churn_rate DESC;
