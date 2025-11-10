
import os

from conf.config import IoT_topic, NB_SONSORS
from src.utils.db_utils import create_mongo_connection
from src.utils.kafka_utils import consumer_message


def consumer_iot(params, logger):
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"simulate.generate_iot_events - EXITING")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(IoT_topic, mongodb_collection, NB_SONSORS, logger)