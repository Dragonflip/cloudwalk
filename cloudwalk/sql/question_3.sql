SELECT		interest_rate,
    		ROUND(SUM(CASE WHEN l.status = 'default' THEN 1 ELSE 0 END)::numeric / COUNT(*), 3) AS default_rate_percentage
FROM	loans as l
	INNER JOIN 	clients as c
		ON c.user_id = l.user_id
GROUP BY 
    interest_rate;
