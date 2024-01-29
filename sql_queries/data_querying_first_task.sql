WITH month_to_month_cohort_cte AS (
	SELECT
		prev_month_table.year_month AS prev_month,
		current_month_table.year_month AS current_month,
		COUNT(prev_month_table.user_uuid) AS active_users
	FROM
		orderrecord_distinct AS prev_month_table
		LEFT JOIN orderrecord_distinct AS current_month_table
			ON prev_month_table.user_uuid = current_month_table.user_uuid
			AND prev_month_table.year_month = (current_month_table.prev_year_month)
	GROUP BY
		current_month,
		prev_month
)
, total_month_active_users_cte AS (
	SELECT
		prev_month,
		SUM(active_users) AS total_month_active_users
	FROM
		month_to_month_cohort_cte
	GROUP BY
		prev_month
)

SELECT 
	month_to_month_cohort_cte.current_month AS year_month,
	tma.total_month_active_users,
	month_to_month_cohort_cte.active_users AS retained_users_count,
	CAST(month_to_month_cohort_cte.active_users AS float) / CAST(tma.total_month_active_users AS float) AS retained_precentage
FROM
	month_to_month_cohort_cte
	JOIN total_month_active_users_cte AS tma
		ON tma.prev_month = month_to_month_cohort_cte.prev_month
WHERE
	1 = 1
	AND current_month is not null