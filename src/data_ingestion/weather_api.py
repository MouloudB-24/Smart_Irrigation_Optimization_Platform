import os
import requests

from src.utils.db_utils import create_mongo_connection, insert_to_mongodb


def query_weather_api(url, api_params, logger):
    
    """summary"""
    
    response = requests.get(url, api_params)
    
    if response.status_code != 200:
        logger.info(f"weather.query_weather_api - Problem in the API request: {response.status_code}")
        return -1
    
    return  response.json()