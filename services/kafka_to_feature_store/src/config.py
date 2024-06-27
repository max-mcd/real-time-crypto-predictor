from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file for local run
load_dotenv(find_dotenv())

# PyDantic loads environment variables automatically 
class Config(BaseSettings):
    kafka_broker_address: str
    kafka_topic: str

    # For Hopsworks Authentication
    hopsworks_api_key: str
    hopsworks_project_name: str

    feature_group_name: str
    feature_group_version: int

config = Config()
