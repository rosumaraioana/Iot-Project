DROP TABLE IF EXISTS iot_data.stg_device_activity;
CREATE TABLE iot_data.stg_device_activity (
    device_id VARCHAR NOT NULL,           -- Unique identifier for the device
    timestamp TIMESTAMP NOT NULL,     -- Timestamp of the activity
    device_type VARCHAR NOT NULL,         -- Type of the device (e.g., Washing Machine, Coffee Machine)
    status VARCHAR NOT NULL,              -- Status of the activity (e.g., Program Start, Program End)
    attributes JSONB                     -- JSONB column to store dynamic attributes
);