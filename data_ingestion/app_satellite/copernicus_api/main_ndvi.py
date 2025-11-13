#####################################################################
#
# Project       : Smart Irrigation Optimiation Platform
#
# File          : main_satellite_temp.py
#
# Description   : main Implementation for retrieving ndvi data
#
# Created       : 12 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

from multiprocessing import Process
from datetime import datetime

from conf.config import BASE_DIR, config_params
from data_ingestion.app_satellite.copernicus_api.kafka_ndvi import consumer_st_ndvi, produce_st_ndvi
from utils.logger import echo_config, logger


def main():
    
    # configure logger
    run_time = datetime.now().strftime("%Y-%m-%d")
    params = config_params()
    log_file = BASE_DIR / "logs" / f"{params["LOGGING_FILE"]}_NDVI_{run_time}.log"
    logger_ = logger(log_file, params["CONSOLE_DEBUG_LEVEL"], params["FILE_DEBUG_LEVEL"])
    
    logger_.debug(f"Starding run, logfile => {log_file}")
    echo_config(params, logger_)
    
    try:
        # produce and store a message in a topic
        p1 = Process(target=produce_st_ndvi, args=(params, logger_))
        
        # consume a message and store it in a mongodb
        p2 = Process(target=consumer_st_ndvi, args=(params, logger_))
        
        # Start process
        p1.start()
        p2.start()

        # Wait process to finish
        p1.join()
        p2.join()
    
    except KeyboardInterrupt:
        logger_.warning("KeyboardInterrupt detected! Terminating all processes...")
        
        # Termnate all processes is Ctrl+C is pressed
        p1.terminate()
        p1.join()
        p2.terminate()
        p2.join()
        
        logger_.info("All processes terminated. Exiting gracefuly!")


if __name__ == "__main__":
    main()
