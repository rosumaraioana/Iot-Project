CREATE TABLE IF NOT EXISTS iot_data.fact_device_failures (
    entry_id SERIAL PRIMARY KEY,        -- Unique identifier of an measurement
    device_id VARCHAR NOT NULL,         -- Foreign key to device dimension
    failure_id INT NOT NULL,          -- Foreign key to failure dimension
    timestamp_utc TIMESTAMP NOT NULL,     -- Timestamp of the activity
    status VARCHAR NOT NULL              -- Activity status
);