import json
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
load_dimensions = DAG("3_load_dimensions", default_args=default_args)

start_operator = DummyOperator(task_id="begin_execution", dag=load_dimensions)
end_operator = DummyOperator(task_id="end_execution", dag=load_dimensions)

load_dim_device = PostgresOperator(
    task_id="load_dim_device",
    sql="sql/load_dimensions/dim_device_insert.sql",
    postgres_conn_id="postgres_local",
    dag=load_dimensions,
)

load_dim_failure = PostgresOperator(
    task_id="load_dim_failure",
    sql="sql/load_dimensions/dim_failure_insert.sql",
    postgres_conn_id="postgres_local",
    dag=load_dimensions,
)

start_operator >> [load_dim_failure, load_dim_device] >> end_operator
