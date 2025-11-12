import requests


def query_weather_api(url, WEATHER_API_PARAMS, logger):
    
    """summary"""
    
    response = requests.get(url, WEATHER_API_PARAMS)
    
    if response.status_code != 200:
        logger.info(f"weather_api.query_weather_api - Problem in the API request: {response.status_code}")
        return -1
    
    return  response.json()