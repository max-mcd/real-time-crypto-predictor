import json
from loguru import logger
from quixstreams import Application

from src.config import config
from src.hopsworks_api import push_data_to_feature_store


def kafka_to_feature_store(
    kafka_broker_address: str,
    kafka_topic: str,
    feature_group_name: str,
    feature_group_version: int,
) -> None:
    """
    Read OHLC data from the Kafka topic and write it to the feature store.
    Write to the feature group specified by a name and a version.

    Args:
        kafka_broker_address (str): Address of the Kafka broker
        kafka_topic (str): Name of the Kafka topic to read from
        feature_group_name (str): Name of the feature group to write data to
        feature_group_version (int): Version of the feature group to write data to

    Returns:
        None
    """

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group="kafka_to_feature_store",
        # process all messages from the input topic when this service starts
        # auto_offset_reset="earliest", 
    )

    # Create a consumer and start a polling loop
    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(1)

            if msg is None:
                continue

            elif msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue

            else:
                # Decode the binary message to a string, then parse it as JSON
                ohlc = json.loads(msg.value().decode("utf-8"))
                #logger.info(f"Received message: {msg.value()}")

                # Write the message to the feature store
                push_data_to_feature_store(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=ohlc,
                )

            # breakpoint()

            # Store the offset of the message in Kafka
            consumer.store_offsets(message=msg)


if __name__ == "__main__":
    kafka_to_feature_store(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )
