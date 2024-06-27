import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file for local run
load_dotenv(find_dotenv())

class Config(BaseSettings):
    """
    Configuration settings for the trade_to_ohlc service

    Attributes:
        kafka_broker_address (str): Address of the Kafka broker
        kafka_input_topic (str): Name of the Kafka topic to read Trades from
        kafka_output_topic (str): Name of the Kafka topic to write OHLC data to
        ohlc_window_seconds (int): Window size in seconds for OHLC aggregation
    """

    kafka_broker_address: str
    kafka_input_topic: str = 'trade'
    kafka_output_topic: str = 'ohlc'
    ohlc_window_seconds: int

config = Config()