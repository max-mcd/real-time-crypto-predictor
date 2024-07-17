import time
from typing import Dict, List

from loguru import logger
from quixstreams import Application

from src.config import config
from src.kraken_api.rest import KrakenRestAPI
from src.kraken_api.websocket import KrakenWebsocketTradeAPI


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_ids: List[str],
    live_or_historical: str,
    last_n_days: int,
) -> None:
    """
    Reads trades from the Kraken websocket API and saves them into a Kafka topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_topic_name (str): The name of the Kafka topic.
        product_ids (List[str]): The product IDs for which to fetch trades.
        live_or_historical (str): Whether to fetch live or historical data.
        last_n_days (int): The number of days to fetch historical data for.

    Returns:
        None
    """
    assert live_or_historical in {"live", "historical"}, f"Invalid value for live_or_historical: {live_or_historical}"

    app = Application(broker_address=kafka_broker_address)

    # The topic where we will save the trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    logger.info(f'Creating the Kraken API to fetch data for {product_ids}')

    # Create the appropriate instance of the Kraken API
    if live_or_historical == 'live':
        logger.info('Creating the Kraken Websocket API to fetch live trade data')
        kraken_api = KrakenWebsocketTradeAPI(product_ids=product_ids)
    else:
        logger.info('Creating the Kraken REST API to fetch historical trade data')
        # Get current timestamp in milliseconds
        to_ms = int(time.time() * 1000)
        from_ms = to_ms - last_n_days * 24 * 60 * 60 * 1000

        kraken_api = KrakenRestAPI(
            product_ids=product_ids,
            from_ms=from_ms,
            to_ms=to_ms,
        )

        logger.info('Creating the producer...')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # Check if we're done fetching historical data
            if kraken_api.is_done():
                logger.info('Done fetching historical data')
                break

            # Fetch a list of trades from the Kraken API
            trades: List[Dict] = kraken_api.get_trades()

            # Iterate over the trades and send them to the Kafka topic
            for trade in trades:
                # Serialize an event using the defined Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Sent trade: {trade}')


if __name__ == '__main__':
    try:
        produce_trades(
            kafka_broker_address=config.kafka_broker_address,
            kafka_topic_name=config.kafka_topic_name,
            product_ids=config.product_ids,

            # Parameters required to run the trade producer for historical data
            live_or_historical=config.live_or_historical,
            last_n_days=config.last_n_days,
        )
    except KeyboardInterrupt:
        logger.info('Exiting the trade producer ...')