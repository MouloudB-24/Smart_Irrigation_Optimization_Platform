#####################################################################
#
# Project       : Smart Irrigation Optimisation Platform
#
# File          : satellite_kafka.py
#
# Description   : Implementation of the satellite data producer kafka
# 
# Created       : 12 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

from logging import Logger
import os

from data_ingestion.app_satellite.nasa_power_api.air_temperature import get_air_temperature
from utils.db_utils import create_mongo_connection
from utils.kafka_utils import consumer_message, produce_message



def produce_air_temp(params: dict, logger: Logger):
    
    """summary"""
        
    # temperature data
    message = get_air_temperature(params["LATITUDE"], params["LONGITUDE"], logger)
    if message == -1:
        os._exit(1)
        
    logger.debug("produce_air_temp - Soil Temperature kafka process:")
    
    # send message to the topic
    produce_message(params["ST_TEMP_TOPIC"], message, logger)
    

def consumer_air_temp(params: dict, logger: Logger):
    
    # Mongodb persistance
    mongodb_collection = create_mongo_connection(params, logger)
    
    if mongodb_collection == -1:
        logger.critical("consumer_air_temp - Exiting")
        os._exit(1)
        
    # Loading data into Mongodb
    consumer_message(params["ST_TEMP_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)
    