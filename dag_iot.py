from datetime import datetime, timedelta
from logging import Logger
from pathlib import Path
import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# add folder project to sys.path
sys.path.append(
    "/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform"
)

from conf.config import BASE_DIR, config_params
from data_processing.etl_iot import extract, load_to_csv, transform
from utils.logger import echo_config, logger


# run_time = datetime.now().strftime("%Y-%m-%d")
params = config_params()
params["MONGO_COLLECTION"] = "sensor_data"

log_file = BASE_DIR / "logs" / params["TODAY"] / f"{params["LOGGING_FILE"]}_ETL_IoT.log"
logger_ = logger(log_file, params["CONSOLE_DEBUG_LEVEL"], params["FILE_DEBUG_LEVEL"])

# logger_.info(f"Starding run, logfile => {log_file}")
# echo_config(params, logger_)


def extract_task_function(params: dict, logger: Logger) -> None:
    extract(params, logger)


def transform_task_function(params: dict, logger: Logger) -> None:
    transform(params, logger)


# # # print(df)
# load_to_csv(df, params, logger_)
# transform(params, logger_)

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

# load_task = PythonOperator(
#     python_callable=load_to_csv,
#     dag=dag,
#     task_id="load_data_to_csv",
#     op_kwargs={"df": extract(params, logger_), "params": params, "logger_": logger_},
# )

# Define pipeline
extract_task >> transform_task
