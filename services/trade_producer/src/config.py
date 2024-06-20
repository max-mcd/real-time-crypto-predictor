import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file for local run
load_dotenv(find_dotenv())

kafka_broker_address=os.environ['KAFKA_BROKER_ADDRESS']
kafka_topic_name='trade'
product_id='BTC/USD'