
from logging import Logger
import os
from data_ingestion.app_weather.weather import get_weather_data
from utils.db_utils import create_mongo_connection
from utils.kafka_utils import consumer_message, produce_message


def produce_weather(params: dict, logger: Logger):
    
    """summary"""
    
    # query api
    message = get_weather_data(logger)
    if message == -1:
        os._exit(1)
    
    logger.info("produce_weather - weather kafka process:")
    
    # send to topic
    produce_message(params["WEATHER_TOPIC"], message, logger)
        

def consumer_weather(params: dict, logger: Logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"consumer_weather - Exiting")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["WEATHER_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)