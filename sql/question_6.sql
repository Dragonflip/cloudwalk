WITH default_rate_year as ( 
SELECT  extract(month from created_at),
		extract(year from created_at),
		SUM(CASE WHEN status='default' THEN loan_amount ELSE 0 END)/SUM(loan_amount) as default_rate
FROM loans
WHERE created_at::date < '2023-11-01'::date
GROUP BY extract(year from created_at), extract(month from created_at)
ORDER BY 2,1
),
default_rate_avg as (
SELECT AVG(default_rate) default_rate_avg
FROM default_rate_year
),
loans_per_year as (
SELECT 		extract(month from created_at) as month,
			extract(year from created_at) as year,
			SUM(CASE
		   		WHEN status = 'paid' THEN amount_paid - loan_amount
		   		ELSE 0
		  	END)::int as paid,
			SUM(CASE
		   		WHEN status = 'default' THEN amount_paid - loan_amount
		   		ELSE 0
		  	END)::int as "default",
			SUM(CASE
		   		WHEN status = 'ongoing' THEN (due_amount - loan_amount)*default_rate_avg
		   		ELSE 0
		  	END)::int as "ongoing"
			
FROM loans
CROSS JOIN default_rate_avg
GROUP BY extract(year from created_at),  extract(month from created_at)
)
SELECT 	"year",
		"month",
		paid + "default" as profit,
		ongoing as ongoing
FROM loans_per_year
ORDER BY year
