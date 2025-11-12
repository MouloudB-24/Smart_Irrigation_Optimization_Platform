
import json
import os
from kafka import KafkaProducer
from kafka import KafkaConsumer

from utils.db_utils import create_mongo_connection, insert_to_mongodb


def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        key_serializer=lambda k: str(k).encode("utf-8"),
        value_serializer=lambda v: v.encode("utf-8")
    )
    
    
def produce_message(topic, json_thing, logger):
    
    """function to send a message to the topic kafka"""
    
    producer = create_kafka_producer()
    
    try:
        if type(json_thing) is not str:
            message = json.dumps(json_thing)
        else:
            message = json_thing
        
        producer.send(topic, message)
        producer.flush()
        
    except Exception as e:
        logger.error(f"Error in the src.utils.kafka_utils.produce_message: {e}")


def create_kafka_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        group_id="iot_consumer_group",
        enable_auto_commit=False,
        # consumer_timeout_ms=2000
    )
    

def consumer_message(topic, my_collection, max_docs, logger):
    
    """function to consume a message from topic kafka and saved it in the mongodb"""
    
    consumer = create_kafka_consumer(topic)
     
    my_docs = []
    
    try:
        
        for msg in consumer:
            
            # Extract information from kafka
            message = json.loads(msg.value.decode("utf-8"))
            
            # Add message to events
            my_docs.append(message)
            
            # break
            if len(my_docs) >= max_docs:
                insert_to_mongodb(my_collection, my_docs, logger)
                consumer.commit()
                
                logger.info(f"src.utils.kafka_utils.consumer_message - messages saved in Mongodb")
                
                # reset
                my_docs = []
                
    except Exception as e:
        logger.error(f"Error in the src.utils.kafka_utils.consumer_message: {e}")
        
    finally:
        consumer.close()
        
        
def consumer_iot(params, logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"simulate.generate_iot_events - EXITING")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["IoT_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)
    

def consumer_weather(params, logger):
    
    """summary"""
    
    # MongoDB persistence
    mongodb_collection = create_mongo_connection(params, logger)

    if mongodb_collection == -1:
        logger.critical(f"simulate.generate_iot_events - EXITING")
        os._exit(1)
    
    # Loading data into Mongodb
    consumer_message(params["WEATHER_TOPIC"], mongodb_collection, params["MAX_DOCS"], logger)