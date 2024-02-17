SELECT  extract(month from created_at) as month,
		extract(year from created_at) as year,
		COUNT(*) as quantity,
		SUM(loan_amount) as value
FROM loans
GROUP BY 1, 2
ORDER BY 3 DESC
