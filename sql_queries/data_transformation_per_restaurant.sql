CREATE TABLE orderrecord_distinct_per_rest (
    year_month INTEGER NOT NULL,
    prev_year_month INTEGER NOT NULL,
    user_uuid CHAR(32) NOT NULL,
    restaurant_uuid CHAR(32) NOT NULL
);

INSERT INTO orderrecord_distinct_per_rest 
    SELECT DISTINCT
        strftime("%Y%m", order_date) AS year_month,
        strftime("%Y%m", order_date) - 1 AS prev_year_month,
        user_uuid,
        restaurant_uuid
    FROM orderrecord;

CREATE INDEX ix__orderrecord_distinct_per_rest__rest_uuid_year_month ON orderrecord_distinct_per_rest (restaurant_uuid,user_uuid, year_month);

CREATE INDEX ix__orderrecord_distinct_per_rest__rest_uuid_prev_year_month ON orderrecord_distinct_per_rest (restaurant_uuid,user_uuid, prev_year_month)