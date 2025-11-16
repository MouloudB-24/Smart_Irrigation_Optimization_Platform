

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

table_initial_attribs = ["timestamp", "name", "deviceType", "sensorType", "measure", "unit"]
raw_data = BASE_DIR/"data"/"raw"
processed_data = BASE_DIR/"data"/"processed"


def extract(raw_data: Path, logger: Logger) -> pd.DataFrame:
    """This function extracts the information from mongodb and save it to a dataframe"""
              
    # connect to db
    mongodb_collection = create_mongo_connection(params, logger)
    if mongodb_collection == -1:
        os._exit(1)

    try:
        
        
        
        
        df = pd.DataFrame(columns=table_initial_attribs)
        
        csv_path = raw_data/"iot_data.csv"
        
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



def load_to_csv(df: pd.DataFrame, raw_data: Path, logger: Logger) -> None:
    """summary"""
    
    try:
        df.to_csv(raw_data/"iot_data.csv", index=False)
            
    except Exception:
        logger.critical("load_to_json - ")
        os._exit(1)
        

def transform(raw_data: Path, processed_data: Path, logger: Logger) -> pd.DataFrame:
    """summary"""

    try:
        df = pd.read_csv(raw_data/"iot_data.csv")
        sites = pd.DataFrame(df["name"].unique(), columns=["name"])
        devices = pd.DataFrame(df["deviceType"].unique(), columns=["deviceType"])
        units = pd.DataFrame(df["unit"].unique(), columns=["unit"])
        
        def save_to_csv(table, table_name):
            table.reset_index()
            table.index.name = "id"
            table.index += 1
            table.to_csv(processed_data/f"{table_name}.csv")

        save_to_csv(sites, "site")
        save_to_csv(devices, "device")
        save_to_csv(units, "unit")
        
        
        sitedevice = df[["name", "deviceType"]].drop_duplicates(subset=["name", "deviceType"])
        # sitedevice["name"] = sitedevice["name"].apply(lambda x: x)
        
        print(sitedevice)
        print(sites)
        
    except Exception:
        logger.exception("transform - ")
        os._exit(1)
    
    
    

if __name__ == "__main__":
    params = {}
    params["MONGO_USERNAME"]="root"
    params["MONGO_PASSWORD"]="mongodbroot"
    params["MONGO_DATABASE"]="irrigation_db"
    params["MONGO_COLLECTION"]="sensor_data"
    
    logger_ = logger("etl_iot.log", 1, 0)

    df = extract(raw_data, logger_)
    
    print(df)

    load_to_csv(df, raw_data, logger_)
    
    
    transform(raw_data, processed_data, logger_)