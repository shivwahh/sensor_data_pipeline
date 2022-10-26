# A simple example demonstrating use of JSONSerializer.

import argparse
from uuid import uuid4
from src.kafka_config import sasl_conf, schema_config
from six.moves import input
from src.kafka_logger import logging
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
import pandas as pd
from typing import List
from src.entity.generic import Generic, instance_to_dict


FILE_PATH = "D:\DATA_SCIENCE\MY_PROJECTS\INEURON\sensor_data_pipeline\sample_data/sensor/aps_failure_training_set1.csv"

def car_to_dict(car:Generic,ctx):

    """
    Return a dict representation of a user instance for serialization.
    Args:
        user (User): User instance.
        ctx (SerializationContext): Metadata pertaining to the serialization operation.
    Returns:
        dict: Dict populated with user attributes to be serialized.
        : param car:
    """
    
    #User._adress must not be serialized; omit from dict
    return car.record
