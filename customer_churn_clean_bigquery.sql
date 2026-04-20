CREATE OR REPLACE VIEW `your_project.your_dataset.customer_churn_clean` AS
WITH staged AS (
  SELECT
    customerID AS customer_id,
    gender,
    SAFE_CAST(SeniorCitizen AS INT64) AS senior_citizen,
    CASE
      WHEN SAFE_CAST(SeniorCitizen AS INT64) = 1 THEN 'Senior'
      ELSE 'Non-senior'
    END AS senior_group,
    Partner AS partner,
    Dependents AS dependents,
    SAFE_CAST(tenure AS INT64) AS tenure_months,
    PhoneService AS phone_service,
    MultipleLines AS multiple_lines,
    InternetService AS internet_service,
    OnlineSecurity AS online_security,
    OnlineBackup AS online_backup,
    DeviceProtection AS device_protection,
    TechSupport AS tech_support,
    StreamingTV AS streaming_tv,
    StreamingMovies AS streaming_movies,
    Contract AS contract,
    PaperlessBilling AS paperless_billing,
    PaymentMethod AS payment_method,
    SAFE_CAST(MonthlyCharges AS NUMERIC) AS monthly_charges,
    SAFE_CAST(NULLIF(TRIM(CAST(TotalCharges AS STRING)), '') AS NUMERIC) AS total_charges,
    Churn AS churn_status,
    CASE
      WHEN Churn = 'Yes' THEN 1
      ELSE 0
    END AS churn_flag,
    CASE
      WHEN SAFE_CAST(tenure AS INT64) <= 6 THEN '0-6 months'
      WHEN SAFE_CAST(tenure AS INT64) <= 12 THEN '7-12 months'
      WHEN SAFE_CAST(tenure AS INT64) <= 24 THEN '13-24 months'
      WHEN SAFE_CAST(tenure AS INT64) <= 48 THEN '25-48 months'
      ELSE '49-72 months'
    END AS tenure_band,
    CASE
      WHEN SAFE_CAST(tenure AS INT64) <= 6 THEN 'Onboarding'
      WHEN SAFE_CAST(tenure AS INT64) <= 12 THEN 'Early relationship'
      WHEN SAFE_CAST(tenure AS INT64) <= 24 THEN 'Mid-term'
      ELSE 'Established'
    END AS tenure_stage,
    CASE
      WHEN SAFE_CAST(MonthlyCharges AS NUMERIC) < 35 THEN '<$35'
      WHEN SAFE_CAST(MonthlyCharges AS NUMERIC) < 70 THEN '$35-$70'
      WHEN SAFE_CAST(MonthlyCharges AS NUMERIC) < 100 THEN '$70-$100'
      ELSE '$100+'
    END AS monthly_charge_band,
    CASE
      WHEN SAFE_CAST(NULLIF(TRIM(CAST(TotalCharges AS STRING)), '') AS NUMERIC) < 500 THEN '<$500'
      WHEN SAFE_CAST(NULLIF(TRIM(CAST(TotalCharges AS STRING)), '') AS NUMERIC) < 1500 THEN '$500-$1.5k'
      WHEN SAFE_CAST(NULLIF(TRIM(CAST(TotalCharges AS STRING)), '') AS NUMERIC) < 3500 THEN '$1.5k-$3.5k'
      ELSE '$3.5k+'
    END AS total_charge_band,
    CASE
      WHEN LOWER(PaymentMethod) LIKE '%automatic%' THEN 'Auto-pay'
      ELSE 'Manual pay'
    END AS payment_mode,
    CASE
      WHEN InternetService = 'No' THEN 'No internet service'
      WHEN OnlineSecurity = 'Yes' AND TechSupport = 'Yes' THEN 'Fully protected'
      WHEN OnlineSecurity = 'No' AND TechSupport = 'No' THEN 'Unprotected'
      ELSE 'Partially protected'
    END AS support_profile,
    (
      CASE WHEN Contract = 'Month-to-month' THEN 1 ELSE 0 END
      + CASE WHEN InternetService = 'Fiber optic' THEN 1 ELSE 0 END
      + CASE WHEN PaymentMethod = 'Electronic check' THEN 1 ELSE 0 END
      + CASE WHEN SAFE_CAST(tenure AS INT64) <= 12 THEN 1 ELSE 0 END
      + CASE WHEN OnlineSecurity = 'No' THEN 1 ELSE 0 END
      + CASE WHEN TechSupport = 'No' THEN 1 ELSE 0 END
    ) AS risk_score,
    (
      CASE WHEN PhoneService = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN MultipleLines = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN InternetService IN ('DSL', 'Fiber optic') THEN 1 ELSE 0 END
      + CASE WHEN OnlineSecurity = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN OnlineBackup = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN DeviceProtection = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN TechSupport = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN StreamingTV = 'Yes' THEN 1 ELSE 0 END
      + CASE WHEN StreamingMovies = 'Yes' THEN 1 ELSE 0 END
    ) AS service_count
  FROM `your_project.your_dataset.customer_churn_raw`
)
SELECT
  *,
  CASE
    WHEN risk_score <= 1 THEN 'Low'
    WHEN risk_score <= 3 THEN 'Moderate'
    WHEN risk_score = 4 THEN 'High'
    ELSE 'Critical'
  END AS risk_segment
FROM staged;
