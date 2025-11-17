
import os
from logging import Logger
from typing import List
import pandas as pd

from utils.db_utils import create_mongo_connection, create_postgre_connection


def extract(params: dict, logger: Logger) -> pd.DataFrame:
    """This function extracts the information from mongodb and save it to a csv file"""
              
    # connect to db
    mongodb_collection = create_mongo_connection(params, logger)
    if mongodb_collection == -1:
        os._exit(1)

    try:
        # Initialize df
        df = pd.DataFrame(columns=["timestamp", "name", "deviceType", "sensorType", "measure", "unit"])
        
        # retrieve data from last 24 hours
        docs = mongodb_collection.find({"timestamp": {"$gt": params["LAST_EXTRACT_DATE"]}})
        
        for doc in docs:
            # flattening metadata
            for key, value in doc["metadata"].items():
                doc[key]= value
            # delete metadata and id
            del  doc["metadata"], doc["_id"]
            
            curr_df = pd.DataFrame.from_dict(doc, orient="index").T
            df = pd.concat([df, curr_df], ignore_index=True)
        
        # Save data
        df.to_csv(f"{params["RAW_DATA_PATH"]}/iot_data_{params["TODAY"]}.csv", index=False)        
        logger.info("extract - IoT data has been extracted")
    
    except Exception as e:
        logger.critical(f"extract  - error when extracting IoT data: {e}")
        os._exit(1)
        

def transform(params: dict, logger: Logger) -> pd.DataFrame:
    """summary"""

    try:
        df = pd.read_csv(f"{params['RAW_DATA_PATH']}/iot_data_{params["TODAY"]}.csv")
        
        processed_data_iot = params["PROCESSED_DATA"]/"iot"
        processed_data_iot.mkdir(exist_ok=True, parents=True)
        
        def save_to_csv(df: pd.DataFrame, table: str, index_name: str="", include_id: bool=True):
            if include_id:
                df.reset_index(drop=True)
                df.index += 1
                df.index.name = index_name
                df.to_csv(processed_data_iot/f"{table}_{params["TODAY"]}.csv", index=True)
            else:
                df.to_csv(processed_data_iot/f"{table}_{params["TODAY"]}.csv", index=False)  
    
        def search_id(df1, df2, col1, col2):
            return df1[col1].apply(lambda x: df2[df2[col2] == x].index[0])
        
        # sites data
        sites = pd.DataFrame(df["name"].unique(), columns=["site_name"])
        save_to_csv(sites, "sites", "site_id")
    
        # devices data
        devices = pd.DataFrame(df["deviceType"].unique(), columns=["device_type"])
        save_to_csv(devices, "devices", "device_id")
    
        # sensors data
        sensors = pd.DataFrame(df[["sensorType", "unit"]].drop_duplicates(subset=["sensorType", "unit"]))
        sensors.rename(columns=({"sensorType": "sensor_type", "unit": "sensor_unit"}), inplace=True)
        save_to_csv(sensors, "sensors", "sensor_id")

        
        # measure data
        measures = df
        measures["site_id"] = measures["name"].apply(lambda x: sites[sites["site_name"] == x].index[0])
        measures["sensor_id"] = search_id(measures, sensors, "sensorType", "sensor_type")
        measures = measures[["timestamp", "sensor_id", "measure"]]
        save_to_csv(measures, "measures", "measure_id")

        logger.info("transform - IoT data bas been transformed")
        
    except Exception as e:
        logger.exception(f"transform - error when transforming IoT data: {e}")
        os._exit(1)
        

def load_to_postgre_db(tables: List, params: dict, logger: Logger) -> None:
    """summary"""
    try:
        params["POSTGRE_USER"]="postgres"
        params["POSTGRE_PASSWORD"]="postgresroot"
        params["POSTGRE_DATABASE"]="iot_db"
        
        engine = create_postgre_connection(params, logger)
        if engine == -1:
            os._exit(1)
    
        processed_data_iot = params["PROCESSED_DATA"]/"iot"
        
        
        for table in tables:
            df = pd.read_csv(processed_data_iot/f"{table}_{params["TODAY"]}.csv")
            
            print(f"Type de engine: {type(engine)}")
            print(f"Engine: {engine}")
            print(f"Tables à charger: {tables}")
            print(f"Colonnes du DataFrame: {df.columns.tolist()}")

            df.to_sql(table, engine, if_exists="append", index=False)
        
            logger.info(f"load_to_postgre_db - IoT data has been loading: {table}")
            
    except Exception as e:
        logger.critical(f"load_to_postgre_db - error when loading IoT data: {e}")
        os._exit(1)
    
    finally:
        engine.dispose()
