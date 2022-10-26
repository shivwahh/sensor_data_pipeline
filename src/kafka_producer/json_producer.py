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

def delivery_report(err,msg):
    """
    Report the success or failure of a message delivery
    Args:
        err (KafkaError): The error that occured on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        logging.info("Delivery failed for User record {}: {} ".format(msg.key(),err))
        return
    logging.info('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(),msg.topic(),msg.partition(),msg.offset()))

def product_data_using_file(topic,file_path):
    schema_str = Generic.get_schema_to_produce_consume_data(file_path=file_path)
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(schema_str,schema_registry_client,instance_to_dict)

    producer = Producer(sasl_conf())

    print("Producing user record to topic {}. ^C to exit".format(topic))
    # While true
    # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
    try:
        for instance in Generic.get_object(file_path=file_path):
            print(instance)
            producer.produce(topic=topic,
                            key=string_serializer(str(uuid4()),instance_to_dict()),
                            value = json_serializer(instance,SerializationContext(topic,MessageField.VALUE)),
                            on_delivery = delivery_report
                            )
    except KeyboardInterrupt:
        pass
    except ValueError:
        print('Invalid input, discarding record...')
        pass

    print("\nFlusing records....")
    producer.flush()

