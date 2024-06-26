import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file for local run
load_dotenv(find_dotenv())


class Config(BaseSettings):
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic: str = os.environ['KAFKA_TOPIC']
    hopsworks_api_key: str = os.environ['HOPSWORKS_API_KEY']
    hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
    feature_group_name: str = os.environ['HOPSWORKS_FEATUREGROUP_NAME']
    feature_group_version: int = os.environ['HOPSWORKS_FEATUREGROUP_VERSION']


config = Config()
