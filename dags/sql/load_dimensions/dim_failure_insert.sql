INSERT INTO iot_data.dim_attribute (attribute_name, unit)
SELECT DISTINCT
    attr.key AS attribute_name,               -- Attribute name (e.g., Temperature, SpinningSpeed)
    CASE
        WHEN attr.key LIKE '%_Unit' THEN attr.value::TEXT  -- Extracts unit when the key has '_Unit'
        ELSE NULL
    END AS unit
FROM
    iot_data.stg_device_activity da,
    jsonb_each(da.attributes) AS attr(key, value)  -- Unrolls JSON object into key-value pairs
WHERE
    da.attributes IS NOT NULL;