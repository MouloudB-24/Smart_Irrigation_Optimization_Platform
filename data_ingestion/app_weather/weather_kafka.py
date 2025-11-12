
from data_ingestion.app_weather.weather_api import query_weather_api
from utils.kafka_utils import produce_message


def produce_weather(params, logger):
    
    """summary"""
    
    # query api
    message = query_weather_api(params["WEATHER_URL"], params["WEATHER_API_PARAMS"], logger)
    
    produce_message(params["WEATHER_TOPIC"], message, logger)
    
    logger.info(f"src.kafka_producer.produce_weather - waether data is sent to topic: {params["WEATHER_TOPIC"]}")