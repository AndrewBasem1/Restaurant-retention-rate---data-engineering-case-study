CREATE TABLE orderrecord_distinct (
    year_month INTEGER NOT NULL,
    prev_year_month INTEGER NOT NULL,
    user_uuid CHAR(32) NOT NULL
);

INSERT INTO orderrecord_distinct 
    SELECT DISTINCT
        strftime("%Y%m", order_date) AS year_month,
        -- the next column will be used to self join the table easily so we can check how ordered both this month and the month previous to it
        strftime("%Y%m", order_date) -1 as prev_year_month,
        user_uuid
    FROM orderrecord;

-- the following two indices are chosen because we will be selfjoining the table using (user_uuid=user_uuid) and (year_month=prev_year_month)
CREATE INDEX ix_orderrecord_user_and_month ON orderrecord_distinct (user_uuid,year_month);

CREATE INDEX ix_orderrecord_user_and_prev_month ON orderrecord_distinct (user_uuid,prev_year_month)