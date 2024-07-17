import os

from typing import List
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file for local run
load_dotenv(find_dotenv())

class Config(BaseSettings):
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic_name: str = 'trade'
    product_ids: List[str] = [
        'ETH/USD',
        'BTC/USD',
        'ETH/EUR',
        'BTC/EUR',
    ]
    live_or_historical: str = 'live'
    last_n_days: int = 1

config = Config()