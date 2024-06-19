from typing import Dict, List

from loguru import logger
from quixstreams import Application

from src.kraken_api import KrakenWebsocketTradeAPI
from src import config


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_id: str,
) -> None:
    """
    Reads trades from the Kraken websocket API and saves them into a Kafka topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_topic_name (str): The name of the Kafka topic.
        product_id (str): The product ID for which to fetch trades.

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_address)

    # The topic where we will save the trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create an instance of the Kraken API
    logger.info('Creating the Kraken API to fetch trade data')
    kraken_api = KrakenWebsocketTradeAPI(product_id=product_id)

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # get_trades() is a method that returns a list of trades from the Kraken API

            trades: List[Dict] = kraken_api.get_trades()

            # Iterate over the trades and send them to the Kafka topic
            for trade in trades:
                # Serialize an event using the defined Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Sent trade: {trade}')


if __name__ == '__main__':
    produce_trades(
        kafka_broker_address=config.kafka_broker_address, 
        kafka_topic_name=config.kafka_topic_name,
        product_id=config.product_id,
    )
