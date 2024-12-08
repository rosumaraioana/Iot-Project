import json
from datetime import datetime, timedelta
from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator


def _read_json_data():
    try:
        with open("dags/dependencies/device_data.json", "r") as file:
            data = json.load(file)
            print("JSON Data:", data)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        raise e


# Function to insert records into PostgreSQL
def _insert_records(ti):
    pg_hook = PostgresHook(postgres_conn_id="postgres_local")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    data = ti.xcom_pull(task_ids="load_json_data")

    for record in data:
        device_id = (record["DeviceId"],)
        timestamp = record["TimestampUTC"]
        device_type = record["DeviceType"]
        status = record["Status"]
        attributes = record["Attributes"]

        cursor.execute(
            "INSERT INTO iot_data.stg_device_activity (device_id, timestamp, device_type, status, attributes) VALUES (%s, %s, %s, %s, %s)",
            (device_id, timestamp, device_type, status, json.dumps(attributes)),
        )
    connection.commit()
    cursor.close()
    connection.close()


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
iot_staging_area = DAG("2_iot_staging_area", default_args=default_args)

start_operator = DummyOperator(task_id="begin_execution", dag=iot_staging_area)
end_operator = DummyOperator(task_id="end_execution", dag=iot_staging_area)


create_staging_table = PostgresOperator(
    task_id="create_staging_table",
    sql="sql/stg_area/staging_table.sql",
    postgres_conn_id="postgres_local",
    dag=iot_staging_area,
)

load_json_data = PythonOperator(
    task_id="load_json_data", python_callable=_read_json_data, dag=iot_staging_area
)

stage_device_data = PythonOperator(
    task_id="load_json_data_to_table",
    python_callable=_insert_records,
    dag=iot_staging_area,
)


(
    start_operator
    >> [create_staging_table, load_json_data]
    >> stage_device_data
    >> end_operator
)
