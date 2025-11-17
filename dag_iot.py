import sys
from typing import List
from airflow import DAG
from logging import Logger
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator

# add folder project to sys.path
sys.path.append("/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform")

from conf.config import BASE_DIR, config_params
from data_processing.etl_iot import extract, load_to_postgre_db, transform
from utils.logger import logger


# run_time = datetime.now().strftime("%Y-%m-%d")
params = config_params()
params["MONGO_COLLECTION"] = "sensor_data"

log_file = BASE_DIR / "logs" / params["TODAY"] / f"{params["LOGGING_FILE"]}_ETL_IoT.log"
logger_ = logger(log_file, params["CONSOLE_DEBUG_LEVEL"], params["FILE_DEBUG_LEVEL"])


def extract_task_function(params: dict, logger: Logger) -> None:
    extract(params, logger)


def transform_task_function(params: dict, logger: Logger) -> None:
    transform(params, logger)
    

def load_task_function(tables: List, params: dict, logger: Logger) -> None:
    load_to_postgre_db(tables, params, logger)


# default args
default_args = {
"owner": "MB",
"start_date": datetime(2025, 11, 16),
"retries": 1,
"retry_delay": timedelta(minutes=5)
}

# Define DAG
dag = DAG(
"etl_iot_data",
default_args=default_args,
schedule="0 12 * * *",
catchup=False
)

# # Define tasks
extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_task_function,
    op_kwargs={"params": params, "logger": logger_},
    dag=dag,
)

transform_task = PythonOperator(
    task_id="tansform_data",
    python_callable=transform_task_function,
    op_kwargs={"params": params, "logger": logger_},
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data_to_postgreSQL",
    python_callable=load_task_function,
    op_kwargs={"tables": ["sites", "devices", "sensors", "measures"], "params": params, "logger": logger_},
    dag=dag,
)

# Define pipeline
extract_task >> transform_task >> load_task

load_to_postgre_db(["sites", "devices", "sensors", "measures"], params, logger_)