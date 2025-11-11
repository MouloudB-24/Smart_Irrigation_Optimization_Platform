#####################################################################
#
# Project       : Smart Irrigation Optimiation Platform
#
# File          : main_weather.py
#
# Description   : Implementation of the sensor data generation process
#
# Created       : 10 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

from datetime import datetime
import os
from dotenv import load_dotenv

from src.data_ingestion.kafka_consumer import consumer_weather
from src.data_ingestion.kafka_producer import produce_weather
from src.utils.logger import echo_config, logger
from conf.config import BASE_DIR, config_params


# Load API KEY
load_dotenv()
API_KEY = os.environ["API_KEY"]


def main():
    
    run_time = datetime.now().strftime("%Y-%m-%d")
    params = config_params()
    log_file = BASE_DIR / "logs" / f"{params["LOGGING_FILE"]}_Weather_{run_time}.log"
    logger_ = logger(log_file, params["CONSOLE_DEBUG_LEVEL"], params["FILE_DEBUG_LEVEL"])
    
    logger_.info(f"Starding run, logfile => {log_file}")
    echo_config(params, logger_)
    
    produce_weather(params, logger_)
    
    consumer_weather(params, logger_)


if __name__ == "__main__":
    main()
