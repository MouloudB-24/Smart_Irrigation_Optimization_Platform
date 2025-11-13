from logging import Logger
import os
import requests
from dotenv import load_dotenv

# Load variable environment
load_dotenv

def get_weather_data(logger: Logger):
    
    """summary"""
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    weather_api_params = {
    "q": "Fougères, FR",
    "appid": os.environ["API_KEY"],
    "units": "metric",
    "lang": "fr",
    }
    
    try:
        response = requests.get(url, weather_api_params)
        response.raise_for_status()
        
        weather_data = response.json()
        logger.info("get_weather_data - WEATHER API - weather data were obtained")
        
        return  weather_data
    
    except requests.exceptions.Timeout:
        logger.critical("get_weather_data - Timeout: the server took too long to respond")
        return -1
    
    except requests.exceptions.ConnectionError:
        logger.critical("get_weather_data - Connexion impossible: server inaccessible")
        return -1
        
    except requests.exceptions.HTTPError as e:
        logger.critical(f"get_weather_data - HTTP error: {e}")
        return -1
    
    except requests.exceptions.RequestException as e:
        logger.critical(f"get_weather_data - Unexpected error: {e}")
        return -1