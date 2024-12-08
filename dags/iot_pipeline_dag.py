# Import the DAG object
import json
from datetime import datetime, timedelta

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator


# Define the default_args dictionary
default_args = {
    "owner": "mara",
    "start_date": datetime(2024, 12, 8),
    "email": ["rosumaraioana@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "schedule": None,  # timedelta(days=1)
    "retries": 2,
    "retry_delay": timedelta(seconds=5),
}

device_data_dataset = Dataset("dags/dependencies/device_data.json")

unique_device_types = ["Washing machine", "Coffee Machine", "Dishwasher"]


def _read_json_data():
    try:
        with open("dags/dependencies/device_data.json", "r") as file:
            data = json.load(file)
            print("JSON Data:", data)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        raise e


def _filter_device_data(device_type: str, ti):
    print(f"Filter data by device: {device_type}")
    # Pull data from XCom
    data = ti.xcom_pull(task_ids="load_json_data")
    if not data:
        raise ValueError(f"No data for device {device_type} found in XCom!")
    device_type_data = [entry for entry in data if entry["DeviceType"] == device_type]
    print(device_type_data)
    return device_type_data


# Instantiate the DAG object
etl_dag = DAG("iot_data_etl", default_args=default_args)

start_operator = DummyOperator(task_id="Begin_execution", dag=etl_dag)
# read_bash = BashOperator(outlets=[device_data_dataset], task_id="producing_task_1", bash_command="sleep 5")
read_json_task = PythonOperator(
    task_id="load_json_data", python_callable=_read_json_data, dag=etl_dag
)
# create_pet_table = PostgresOperator(
#     task_id="create_pet_table",
#     sql="sql/schema.sql",
#     postgres_conn_id="postgres_local",
#     dag=etl_dag,
# )

filter_tasks = []
for device_type in unique_device_types:
    filter_task = PythonOperator(
        task_id=f"process_device_type_{device_type.replace(' ', '_')}",
        python_callable=_filter_device_data,
        op_args=[device_type],
        dag=etl_dag,
    )
    filter_tasks.append(filter_task)


# task2 = PostgresOperator(
#     task_id='insert_into_table',
#     postgres_conn_id='postgres_local',
#     sql="""
#         insert into Orders values(2,'delivered')
#     """
# )

start_operator >> read_json_task >> filter_tasks


if __name__ == "__main__":
    _read_json_data()
