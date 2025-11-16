

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
        
        def save_to_csv(table: pd.DataFrame, table_name: str, index_name: str="", include_id: bool=True):
            if include_id:
                table.reset_index(drop=True)
                table.index += 1
                table.index.name = index_name
                table.to_csv(processed_data/f"{table_name}.csv", index=True)
            else:
                table.to_csv(processed_data/f"{table_name}.csv", index=False)  
    
        def search_id(df1, df2, col1, col2):
            return df1[col1].apply(lambda x: df2[df2[col2] == x].index[0])
        
        # sites table
        sites = pd.DataFrame(df["name"].unique(), columns=["site_name"])
        save_to_csv(sites, "sites", "site_id")
        
        # devices table
        devices = pd.DataFrame(df["deviceType"].unique(), columns=["device_type"])
        save_to_csv(devices, "devices", "device_id")
        
        # sites_devicess table (many to many)
        sites_devices = df[["name", "deviceType"]].drop_duplicates(subset=["name", "deviceType"])
        sites_devices["site_id"] = search_id(sites_devices, sites, "name", "site_name")
        sites_devices["device_type"] = search_id(sites_devices, devices, "deviceType", "device_type")
        sites_devices = sites_devices[["site_id", "device_type"]]
        save_to_csv(sites_devices, "sites_devices", include_id=False)
        
        # sensors table
        sensors = pd.DataFrame(df[["sensorType", "unit"]].drop_duplicates(subset=["sensorType", "unit"]))
        sensors.rename(columns=({"sensorType": "sensor_type", "unit": "sensor_unit"}), inplace=True)
        save_to_csv(sensors, "sensors", "sensor_id")
        
        # devicesensor table (many to many)
        devices_sensors = df[["deviceType", "sensorType"]].drop_duplicates(subset=["deviceType", "sensorType"])
        devices_sensors["device_id"] = search_id(devices_sensors,devices,  "deviceType", "device_type")
        devices_sensors["sensor_id"] = search_id(devices_sensors, sensors, "sensorType", "sensor_type")
        devices_sensors = devices_sensors[["device_id", "sensor_id"]]
        save_to_csv(devices_sensors, "devices_sensors", include_id=False)
        
        # measure table
        measures = df
        measures["site_id"] = measures["name"].apply(lambda x: sites[sites["site_name"] == x].index[0])
        measures["device_id"] = search_id(measures, devices, "deviceType", "device_type")
        measures["sensor_id"] = search_id(measures, sensors, "sensorType", "sensor_type")
        measures = measures[["timestamp", "site_id", "device_id", "sensor_id", "measure"]]
        save_to_csv(measures, "measures", "measure_id")
        
    except Exception as e:
        logger.exception(f"transform - unexpected error: {e}")
        os._exit(1)

if __name__ == "__main__":
    params = {}
    params["MONGO_USERNAME"]="root"
    params["MONGO_PASSWORD"]="mongodbroot"
    params["MONGO_DATABASE"]="irrigation_db"
    params["MONGO_COLLECTION"]="sensor_data"
    
    logger_ = logger("etl_iot.log", 1, 0)

    df = extract(raw_data, logger_)
    

    load_to_csv(df, raw_data, logger_)
    
    
    transform(raw_data, processed_data, logger_)