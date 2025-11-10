#####################################################################
#
# Project       : Smart Irrigation Optimiation Platform
#
# File          : main.py
#
# Description   : Implementation of the sensor data generation process
#
# Created       : 1 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

from datetime import datetime
from multiprocessing import Process

from conf.config import BASE_DIR
from src.data_ingestion.kafka_consumer import consumer_iot
from src.data_ingestion.kafka_producer import produce_iot
from src.utils.logger import config_params, echo_config, logger


def main():
    
    """_summary_"""
    
    run_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    params = config_params()
    log_file = BASE_DIR / "logs" / f"{params["LOGGING_FILE"]}_{run_time}.log"
    logger_ = logger(log_file, params["CONSOLE_DEBUG_LEVEL"], params["FILE_DEBUG_LEVEL"])
    
    logger_.info(f"Starding run, logfile => {log_file}")
    echo_config(params, logger_)
    
    try:
        p1 = Process(target=produce_iot, args=(params, logger_))
        p2 = Process(target=consumer_iot, args=(params, logger_))

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
                                 
                                 
                                 
                                 
                    