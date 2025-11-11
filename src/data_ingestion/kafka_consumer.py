#####################################################################
#
# Project       : Smart Irrigation Optimisation Platform
#
# File          : kafka_producer.py
#
# Description   : Implementation of the iot data consumer kafka
# 
# Created       : 7 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

import os

from src.utils.db_utils import create_mongo_connection
from src.utils.kafka_utils import consumer_message


def consumer_iot(params, logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"simulate.generate_iot_events - EXITING")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["IoT_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)
    


def consumer_weather(params, logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"simulate.generate_iot_events - EXITING")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["WEATHER_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)