import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file for local run
load_dotenv(find_dotenv())

class Config(BaseSettings):
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_input_topic: str = 'trade'
    kafka_output_topic: str = 'ohlc'
    ohlc_window_seconds: int = os.environ['OHLC_WINDOW_SECONDS']

config = Config()