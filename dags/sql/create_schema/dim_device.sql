CREATE TABLE IF NOT EXISTS iot_data.dim_device (
    device_id VARCHAR PRIMARY KEY,        -- Unique identifier for a device, FK
    device_type VARCHAR NOT NULL          -- Type of the device
);