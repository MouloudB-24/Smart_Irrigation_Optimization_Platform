from datetime import date, datetime, time, timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

# Load var env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

TP_API_PARAMS = {
    "parameters": "T2M",
    "community": "AG",
    "longitude": 2.95,
    "latitude": 48.80,
    "start": 2018111,
    "end": 20181111,
    "format": "JSON",
}


def config_params():
    """Retreive Common Config Pamameters in a dictionary format"""

    params = os.environ

    return {
        # General parameters
        "CONSOLE_DEBUG_LEVEL": int(params.get("CONSOLE_DEBUG_LEVEL", "1")),
        "FILE_DEBUG_LEVEL": int(params.get("FILE_DEBUG_LEVEL", "0")),
        "LOGGING_FILE": params.get("LOGGING_FILE", "logger"),
        "MAX_DOCS": int(params.get("MAX_DOCS", 1)),
        
        # IoT parameters
        "INPUT_DATA_FILE": params.get("INPUT_DATA_FILE", ""),
        "IoT_TOPIC": params.get("IoT_TOPIC", ""),
        "SITE_IDS": params.get("SITE_IDS", 1),
        
        # API weather parameters
        "WEATHER_TOPIC": params.get("WEATHER_TOPIC", ""),
        
        # API NASA
        "LATITUDE": float(params.get("LATITUDE", 0.0)),
        "LONGITUDE": float(params.get("LONGITUDE", 0.0)),
        "ST_TEMP_TOPIC": params.get("ST_TEMP_TOPIC"),
        
        # API NDVI
        "BBOX_COORDS": [float(x) for x in params.get("BBOX_COORDS", "1.240,48.320,-1.150,48.380").split(",")],
        "NDVI_TOPIC": params.get("NDVI_TOPIC"),
        
        # API Earth Engine
        "START_DATE": params.get("START_DATE"),
        "END_DATE": params.get("END_DATE"),
        "ET_TOPIC": params.get("ET_TOPIC"),
        
        # Mongodb parameters
        "MONGO_USERNAME": params["MONGO_USERNAME"],
        "MONGO_PASSWORD": params["MONGO_PASSWORD"],
        "MONGO_DATABASE": "irrigation_db",
        "MONGO_COLLECTION": params.get("MONGO_COLLECTION"),
        
        # Data folder
        "RAW_DATA_PATH": BASE_DIR/"data"/"raw",
        "PROCESSED_DATA": BASE_DIR/"data"/"processed",
        
        # ETL
        "LAST_EXTRACT_DATE": datetime.combine(datetime.today().date() - timedelta(days=1), time(12, 0, 0)),
        "TODAY": str(date.today())
    }
