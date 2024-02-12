WITH loans_per_user as(
SELECT 	c.user_id,
		SUM(loan_amount) as loan_amount,
		SUM(CASE 
				WHEN l.status = 'default' THEN  loan_amount
				ELSE 0
		   END) as amount_default,
		SUM(CASE 
				WHEN l.status <> 'default' THEN  loan_amount
				ELSE 0
		   END) as amount_loans,
		SUM(loan_amount) / SUM(credit_limit) AS credit_utilization_ratio
FROM clients as c
INNER JOIN loans as l
	ON	c.user_id = l.user_id
GROUP BY c.user_id
ORDER BY 4 DESC, 2 DESC
),
max_loans as (
SELECT MAX(loan_amount) as max_loans
FROM loans_per_user
),
user_metrics as (
SELECT 	user_id,
		(amount_loans/(amount_default + amount_loans)) as default_ratio,
		(CASE
		 WHEN credit_utilization_ratio < 0.1 THEN 10*(credit_utilization_ratio)
		 WHEN credit_utilization_ratio <= 0.3 AND credit_utilization_ratio >= 0.1 THEN 1
		 ELSE 1 - (credit_utilization_ratio - 0.3) / 0.7
		 END) as credit_ratio,
		credit_utilization_ratio,
		amount_loans,
		amount_default
FROM loans_per_user
)
SELECT 	user_id,
		(default_ratio*0.35 + credit_ratio*0.5 + (amount_loans/max_loans)*0.15)  as user_metric
FROM user_metrics
CROSS JOIN max_loans
ORDER BY 2 DESC
LIMIT 10
---

WITH loans_per_user as(
SELECT 	c.user_id,
		SUM(loan_amount) as loan_amount,
		SUM(CASE 
				WHEN l.status = 'default' THEN  loan_amount
				ELSE 0
		   END) as amount_default,
		SUM(CASE 
				WHEN l.status <> 'default' THEN  loan_amount
				ELSE 0
		   END) as amount_loans,
		SUM(loan_amount) / SUM(credit_limit) AS credit_utilization_ratio
FROM clients as c
INNER JOIN loans as l
	ON	c.user_id = l.user_id
GROUP BY c.user_id
ORDER BY 4 DESC, 2 DESC
),
max_loans as (
SELECT MAX(loan_amount) as max_loans
FROM loans_per_user
),
user_metrics as (
SELECT 	user_id,
		(amount_loans/(amount_default + amount_loans)) as default_ratio,
		(CASE
		 WHEN credit_utilization_ratio < 0.1 THEN 10*(credit_utilization_ratio)
		 WHEN credit_utilization_ratio <= 0.3 AND credit_utilization_ratio >= 0.1 THEN 1
		 ELSE 1 - (credit_utilization_ratio - 0.3) / 0.7
		 END) as credit_ratio,
		credit_utilization_ratio,
		amount_loans,
		amount_default
FROM loans_per_user
)
SELECT 	user_id,
		(default_ratio*0.35 + credit_ratio*0.5 + (amount_loans/max_loans)*0.15)  as user_metric
FROM user_metrics
CROSS JOIN max_loans
ORDER BY 2 ASC
LIMIT 10
