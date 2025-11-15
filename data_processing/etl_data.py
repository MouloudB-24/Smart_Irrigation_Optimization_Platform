

from datetime import datetime
import json
import os
from logging import Logger
from pathlib import Path
from typing import List
import pandas as pd
from pprint import pprint


from conf.config import BASE_DIR
from utils.db_utils import create_mongo_connection
from utils.logger import logger

table_initial_attribs = ["timestamp", "siteId", "deviceType", "sensorType", "measure", "unit"]
csv_path = Path(BASE_DIR/"data"/"raw"/"iot_data.csv")


def extract(csv_path: Path, logger: Logger) -> pd.DataFrame:
    """This function extracts the information from mongodb and save it to a dataframe"""
              
    # connect to db
    mongodb_collection = create_mongo_connection(params, logger)
    if mongodb_collection == -1:
        os._exit(1)

    try:
        df = pd.DataFrame(columns=table_initial_attribs)
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            last_extract_date = df["timestamp"][df.index[-1]]
        else:
            last_extract_date = datetime(1900, 1, 1)   
                 
        docs = mongodb_collection.find({"timestamp": {"$gt": last_extract_date}})
        
        for doc in docs:
            # flattening metadata
            for key, value in doc["metadata"].items():
                doc[key]= value
            # delete metadata and id
            del  doc["metadata"], doc["_id"]
            
            curr_df = pd.DataFrame.from_dict(doc, orient="index").T
            df = pd.concat([df, curr_df], ignore_index=True)
        return df
    
    except Exception:
        logger.critical("extract - ")
        os._exit(1)



def load_to_csv(df: pd.DataFrame, csv_path: Path, logger: Logger) -> None:
    """summary"""
    
    try:
        df.to_csv(csv_path, index=False)
            
    except Exception:
        logger.critical("load_to_json - ")
        os._exit(1)
        

def transform(data: List, logger: Logger) -> pd.DataFrame:
    """summary"""

    last_extract_date = datetime(1900, 1, 1)
    
    if data:
        last_extract_date = datetime.fromisoformat(data[-1]["timestamp"])
    
    # connect to db
    mongodb_collection = create_mongo_connection(params, logger)
    if mongodb_collection == -1:
        os._exit(1)
    
    docs = mongodb_collection.find({"timestamp": {"$gt": last_extract_date}})
    
    df = pd.DataFrame(columns=table_initial_attribs)
    
    for doc in docs:
        doc["timestamp"] = doc["timestamp"].isoformat()
        for key, value in doc["metadata"].items():
            doc[key]= value
        del  doc["metadata"]
        del doc["_id"]
        curr_df = pd.DataFrame.from_dict(doc, orient="index").T
        df = pd.concat([df, curr_df], ignore_index=True)
    
    return df
    
    

if __name__ == "__main__":
    params = {}
    params["MONGO_USERNAME"]="root"
    params["MONGO_PASSWORD"]="mongodbroot"
    params["MONGO_DATABASE"]="irrigation_db"
    params["MONGO_COLLECTION"]="sensor_data"
    
    logger_ = logger("etl_iot.log", 1, 0)

    df = extract(csv_path, logger_)

    load_to_csv(df, csv_path, logger)
    
    
    # load_to_json(new_data, logger_)