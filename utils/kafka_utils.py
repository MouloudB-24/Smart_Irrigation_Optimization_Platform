
from datetime import datetime
import json
from logging import Logger
import os
from typing import List
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from utils.db_utils import insert_to_mongodb


def create_kafka_producer():
    """configure kfka Producer"""
    
    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        key_serializer=lambda k: str(k).encode("utf-8"),
        value_serializer=lambda v: v.encode("utf-8"))
    
    
def produce_message(topic: str, message_json, logger: Logger):
    """function to send a message to the topic kafka"""
    
    
    try:
        producer = create_kafka_producer()
        
        if type(message_json) is not str:
            message_str = json.dumps(message_json)
        else:
            message_str = message_json
        
        producer.send(topic, message_str)
        producer.flush()
        
        logger.info(f"produce_message - message was send to the topic: {topic}")
    
    except NoBrokersAvailable as e:
        logger.critical(f"produce_message - error connecting to kafka: {e}")
        os._exit(1)
        
    except Exception as e:
        logger.error(f"produce_message - unexpected error : {e}")
        os._exit()


def create_kafka_consumer(topic: str):
    return KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        group_id="iot_consumer_group",
        enable_auto_commit=False,
        consumer_timeout_ms=10000)

 
def consumer_message(topic: str, my_collection: str, max_docs: List, logger: Logger):
    """function to consume a message from topic kafka and saved it in the mongodb"""
         
    my_docs = []
    
    try:
        consumer = create_kafka_consumer(topic)
        
        for msg in consumer:
            
            # Extract information from kafka
            message = json.loads(msg.value.decode("utf-8"))
            
            # convet date str -> objet
            message["timestamp"] = datetime.fromisoformat(message["timestamp"])
            
            # Add message to events
            my_docs.append(message)
            
            # break
            if len(my_docs) >= max_docs:
                logger.info(f"consumer_message - message was consumed from topic: {topic}")
                logger.debug(my_docs)
                
                insert_to_mongodb(my_collection, my_docs, logger)
                consumer.commit()
                
                logger.info("consumer_message - messages saved in Mongodb")
                
                # reset
                my_docs = []
                
        consumer.close()
    
    except NoBrokersAvailable as e:
        logger.critical(f"consumer_message - error connecting to kafka: {e}")
        os._exit(1)
                    
    except Exception as e:
        logger.error(f"consumer_message - unexpected error: {e}")
        os._exit(1)        