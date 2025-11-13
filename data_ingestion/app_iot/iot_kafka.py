#####################################################################
#
# Project       : Smart Irrigation Optimisation Platform
#
# File          : kafka_producer.py
#
# Description   : Implementation of the iot data producer kafka
# 
# Created       : 7 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

from datetime import datetime
from logging import Logger
import os

from conf.config import BASE_DIR
from data_ingestion.app_iot.iot_simulator import simulate_iot
from utils.db_utils import create_mongo_connection
from utils.json_utils import pp_json, read_input_data
from utils.kafka_utils import consumer_message, produce_message


def produce_iot(params, logger):
    
    """_summary_"""
    
    # Load data site
    sites = read_input_data(BASE_DIR / "conf" / params["INPUT_DATA_FILE"], logger)
    
    # quit: problem in the input data file
    if sites == -1:
        os._exit(1)
        
    # Date source
    site = sites[0]
    
    # Start ESP: Kafka   
    logger.info(f"producer_iot.main - Site ID {site["siteId"]}: Starding ESP Kafka")
        
    current_time = datetime.now()

    for device in site["devices"]:

        for sensor in device["sensors"]:
            # new event
            message = simulate_iot(site["name"], device, sensor, current_time, logger)            
    
            # send event to topic
            produce_message(params["IoT_TOPIC"], message, logger)

      
def consumer_iot(params: dict, logger: Logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"simulate.generate_iot_events - EXITING")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["IoT_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)
    
    
    
    
    
    