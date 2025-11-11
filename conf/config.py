import os
from pathlib import Path
from dotenv import load_dotenv

# Load var env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

API_PARAMS= {"q": "Fougères, FR", "appid": os.environ["API_KEY"], "units": "metric", "lang": "fr"}


def config_params():
    
    """Retreive Common Config Pamameters in a dictionary format"""
    
    return {
        # General parameters
        "CONSOLE_DEBUG_LEVEL": int(os.environ["CONSOLE_DEBUG_LEVEL"]),
        "FILE_DEBUG_LEVEL": int(os.environ["FILE_DEBUG_LEVEL"]),
        "LOGGING_FILE": os.environ["LOGGING_FILE"],
        
        # IoT parameters
        "INPUT_DATA_FILE": os.environ.get("INPUT_DATA_FILE", ""),
        "IoT_TOPIC": os.environ.get("IoT_TOPIC", "IoT_TOPIC"),
        "SITE_IDS": os.environ.get("SITE_IDS", 1),
        "MAX_DOCS": int(os.environ.get("MAX_DOCS", 12)),
        
        # Api weather parameters
        "API_PARAMS": API_PARAMS,
        "BASE_URL": os.environ.get("BASE_URL"),
        "WEATHER_TOPIC": os.environ.get("WEATHER_TOPIC", "WEATHER_TOPIC"),
              
        # Mongodb parameters
        "MONGO_USERNAME": os.environ["MONGO_USERNAME"],
        "MONGO_PASSWORD": os.environ["MONGO_PASSWORD"],
        "MONGO_DATABASE": os.environ["MONGO_DATABASE"],
        "MONGO_COLLECTION": os.environ["MONGO_COLLECTION"]
    }