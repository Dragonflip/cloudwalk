SELECT	extract(month from l.created_at) as month, 
		extract(year from l.created_at) as year,
		SUM(CASE 
			WHEN l.status = 'default' THEN  loan_amount
			ELSE 0
	   	END)/SUM(loan_amount) as default_rate
FROM loans as l
INNER JOIN clients as c
	ON	c.user_id = l.user_id
GROUP BY extract(month from l.created_at), extract(year from l.created_at)
ORDER BY 2, 1

---
SELECT	c.batch,
		SUM(CASE 
			WHEN l.status = 'default' THEN  loan_amount
			ELSE 0
	   	END)/SUM(loan_amount) as default_rate
FROM loans as l
INNER JOIN clients as c
	ON	c.user_id = l.user_id
GROUP BY c.batch
ORDER BY 1
