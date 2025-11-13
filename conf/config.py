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

    prs = os.environ

    return {
        # General parameters
        "CONSOLE_DEBUG_LEVEL": int(prs["CONSOLE_DEBUG_LEVEL"]),
        "FILE_DEBUG_LEVEL": int(prs["FILE_DEBUG_LEVEL"]),
        "LOGGING_FILE": prs["LOGGING_FILE"],
        # IoT parameters
        "INPUT_DATA_FILE": prs.get("INPUT_DATA_FILE", ""),
        "IoT_TOPIC": prs.get("IoT_TOPIC", ""),
        "SITE_IDS": prs.get("SITE_IDS", 1),
        "MAX_DOCS": int(prs.get("MAX_DOCS", 12)),
        # API weather parameters
        "WEATHER_TOPIC": prs.get("WEATHER_TOPIC", ""),
        # API NASA
        "LATITUDE": float(prs.get("LATITUDE", 0.0)),
        "LONGITUDE": float(prs.get("LONGITUDE", 0.0)),
        "ST_TEMP_TOPIC": prs.get("ST_TEMP_TOPIC"),
        # API NDVI
        "BBOX_COORDS": [float(x) for x in prs.get("BBOX_COORDS", "1.240,48.320,-1.150,48.380").split(",")],
        "TIME_INTERVAL": tuple(prs.get("TIME_INTERVAL", "2025-06-01,2025-06-01").split(",")),
        "NDVI_TOPIC": prs.get("NDVI_TOPIC"),
        # API Earth Engine
        "START_DATE": prs.get("START_DATE"),
        "END_DATE": prs.get("END_DATE"),
        "ET_TOPIC": prs.get("ET_TOPIC"),
        # Mongodb parameters
        "MONGO_USERNAME": prs["MONGO_USERNAME"],
        "MONGO_PASSWORD": prs["MONGO_PASSWORD"],
        "MONGO_DATABASE": prs["MONGO_DATABASE"],
        "MONGO_COLLECTION": prs["MONGO_COLLECTION"],
    }
