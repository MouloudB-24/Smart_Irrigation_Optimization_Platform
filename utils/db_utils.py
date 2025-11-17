#####################################################################
#
# Project       : IoT based TimesSeries Data via Python Application
#
# File          : connection_db.py
#
# Description   : Function for use to persist the data to file and MongoDB
# 
#                 Options:
#                       - site["data_persistence"] = 0 => None
#                       - site["data_persistence"] = 1 => File
#                       - site["data_persistence"] = 2 => MongoDB
#
# Created       : 3 November 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

from logging import Logger
from typing import List
import pymongo
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def create_mongo_connection(params: dict, logger: Logger) -> pymongo.collection:
    
    """Connect to the MongoDB database 'IoTSensor_db' """
    
    try:
        if params["MONGO_USERNAME"] != "":
            MONGO_URI = f"mongodb://{params["MONGO_USERNAME"]}:{params["MONGO_PASSWORD"]}@localhost:27017/?directConnection=true"
        else:
            MONGO_URI = "mongodb://localhost:27017/?directConnection=true"
    
        logger.debug(f"create_mongo_connection - URI: {MONGO_URI}")

        try:
            connection = pymongo.MongoClient(MONGO_URI)
            connection.admin.command("ping")
            
        except pymongo.errors.ServerSelectionTimeoutError:
            logger.critical(f"create_mongo_connection - mongo server took too long to respond!")
            return -1
        
        my_database = connection[params["MONGO_DATABASE"]]
        my_collection = my_database[params["MONGO_COLLECTION"]]
        
        logger.info(f"create_mongo_connection - CONNECTED")
        
        return my_collection
    
    except Exception as e:
        logger.critical(f"create_mongo_connection - FAILED error: {e}")
        return -1 
        

def insert_to_mongodb(my_collection: pymongo.collection, events: List, logger: Logger):
    
    """Insert one or many document into the MongoDB collection"""
    
    try:  
        return my_collection.insert_many(events)
    
    except pymongo.errors.PyMongoError as e:
        logger.error(f"connection.insertOne - insert_many - FAILED: {e} ")
        return -1


def create_postgre_connection(params: dict, logger: Logger):
    """summary"""
    
    try:
        engine = create_engine(
            f'postgresql+psycopg2://{params["POSTGRE_USER"]}:{params["POSTGRE_PASSWORD"]}'
            f'@localhost:5432/{params["POSTGRE_DATABASE"]}'
            )
        
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            
        return engine
    
    except SQLAlchemyError as e:
        logger.critical(f"create_postgresql_connection - connection postgreSQL error:")
        return -1
    