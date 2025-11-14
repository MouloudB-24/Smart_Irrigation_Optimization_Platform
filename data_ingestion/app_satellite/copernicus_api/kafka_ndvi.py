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

from data_ingestion.app_satellite.copernicus_api.ndvi import get_st_ndvi
from utils.db_utils import create_mongo_connection
from utils.kafka_utils import consumer_message, produce_message


def produce_st_ndvi(params: dict, logger: Logger):
    """summary"""
    
    logger.info("produce_st_mdvi - kfka process: NDVI")
    
    message = get_st_ndvi(params["BBOX_COORDS"], logger)
    if message == -1:
        os._exit(1)
    
    logger.info("produce_st_ndvi - weather kafka process:")
    
    # send to topic
    produce_message(params["NDVI_TOPIC"], message, logger)


def consumer_st_ndvi(params: dict, logger: Logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"consumer_st_ndvi - Exiting")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["NDVI_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)
    
    