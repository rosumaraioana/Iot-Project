CREATE TABLE IF NOT EXISTS iot_data.facts_device_activity (
    entry_id SERIAL PRIMARY KEY,        -- Unique identifier of an measurement
    device_id VARCHAR NOT NULL,         -- Foreign key to device dimension
    attribute_id INT NOT NULL,          -- Foreign key to attribute dimension
    timestamp_utc TIMESTAMP NOT NULL,     -- Timestamp of the activity
    status VARCHAR NOT NULL,              -- Activity status
    value INT NOT NULL                    -- Actual value
);