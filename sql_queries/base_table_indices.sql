CREATE INDEX ix__orderrecord__overall_retention_rate ON orderrecord (user_uuid, order_date_year_month);

CREATE INDEX ix__orderrecord__per_restaurant_retention_rate ON orderrecord (restaurant_uuid, user_uuid, order_date_year_month)
