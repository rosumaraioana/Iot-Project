CREATE TABLE IF NOT EXISTS iot_data.dim_attribute (
    attribute_id SERIAL PRIMARY KEY,      -- Unique identifier of an attribute, FK
    attribute_name VARCHAR NOT NULL,      -- Name of the attribute
    unit VARCHAR                          -- Unit of measuremet
);