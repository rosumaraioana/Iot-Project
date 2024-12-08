CREATE TABLE  IF NOT EXISTS iot_data.dim_failure (
    failure_id SERIAL PRIMARY KEY,     -- Unique identifier, FK
    failure_code INT NOT NULL          -- Code for the failure
);