from datetime import datetime, timedelta
from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator


# Define the default_args dictionary
default_args = {
    "owner": "mara",
    "start_date": datetime(2023, 1, 1),
    "email": ["rosumaraioana@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "schedule": None,  # timedelta(days=1)
    "retries": 0,
}

# Instantiate the DAG object
iot_data_setup_database = DAG("1_iot_data_setup_database", default_args=default_args)

start_operator = DummyOperator(task_id="begin_execution", dag=iot_data_setup_database)
end_operator = DummyOperator(task_id="end_execution", dag=iot_data_setup_database)

create_iot_schema = PostgresOperator(
    task_id="create_schema",
    sql="sql/create_schema/schema.sql",
    postgres_conn_id="postgres_local",
    dag=iot_data_setup_database,
)

create_dim_device = PostgresOperator(
    task_id="create_dim_device",
    sql="sql/create_schema/dim_device.sql",
    postgres_conn_id="postgres_local",
    dag=iot_data_setup_database,
)

create_dim_failure_details = PostgresOperator(
    task_id="create_dim_failure_details",
    sql="sql/create_schema/dim_failure.sql",
    postgres_conn_id="postgres_local",
    dag=iot_data_setup_database,
)

create_dim_attribute_details = PostgresOperator(
    task_id="create_dim_attribute_details",
    sql="sql/create_schema/dim_attribute.sql",
    postgres_conn_id="postgres_local",
    dag=iot_data_setup_database,
)

create_facts_device_activity = PostgresOperator(
    task_id="create_facts_device_activity",
    sql="sql/create_schema/facts_device_activity.sql",
    postgres_conn_id="postgres_local",
    dag=iot_data_setup_database,
)

create_facts_device_failures = PostgresOperator(
    task_id="create_facts_device_failures",
    sql="sql/create_schema/facts_device_failures.sql",
    postgres_conn_id="postgres_local",
    dag=iot_data_setup_database,
)

(
    start_operator
    >> create_iot_schema
    >> [create_dim_failure_details, create_dim_attribute_details, create_dim_device]
    >> create_facts_device_activity
    >> create_facts_device_failures
    >> end_operator
)
