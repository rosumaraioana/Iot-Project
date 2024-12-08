INSERT INTO iot_data.dim_device (device_id, device_type)
SELECT DISTINCT
    device_id::VARCHAR,
    device_type::VARCHAR
FROM iot_data.stg_device_activity
