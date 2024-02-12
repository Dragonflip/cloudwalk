WITH UserAdherence AS (
    SELECT 
        batch,
        SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) AS approved_users,
        COUNT(*) AS total_users,
		ROUND(SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END)::numeric/COUNT(*)::numeric, 2) as user_approved_rate
    FROM 
        Clients
    GROUP BY 
        batch
),
LoanAdherence AS (
    SELECT 
        batch,
        SUM(CASE WHEN l.status = 'paid' THEN 1 ELSE 0 END) AS paid_loans,
        COUNT(*) AS total_loans,
		ROUND(SUM(CASE WHEN l.status != 'default' THEN 1 ELSE 0 END)::numeric/COUNT(*)::numeric, 2) as loans_paid_rate
    FROM 
        Loans l
    JOIN 
        Clients c ON l.user_id = c.user_id
    GROUP BY 
        batch
)

SELECT 	u.batch as batch,
		u.user_approved_rate,
		l.loans_paid_rate,
		u.user_approved_rate * l.loans_paid_rate as adherence_rate
FROM UserAdherence as u
INNER JOIN LoanAdherence as l
	ON l.batch = u.batch
ORDER BY 4 desc
LIMIT 1
