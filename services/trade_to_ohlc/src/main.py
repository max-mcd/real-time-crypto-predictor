from datetime import timedelta

from quixstreams import Application
from loguru import logger

from src.config import config


def trade_to_ohlc(
		kafka_input_topic: str,
		kafka_output_topic: str,
		kafka_broker_address: str,
		ohlc_window_seconds: int,
) -> None:
    """
    This function reads trades from the kafka input topic
    Aggregates them into OHLC candles using the specified window in `ohlc_window_seconds`
    Saves the ohlc data into another kafka topic
    
    Args:
        kafka_input_topic (str): Kafka topic to read trade data from
        kafka_output_topic (str): Kafka topic to write OHLC candles to
        kafka_broker_address (str): Kafka broker address
        ohlc_window_seconds (int): Window size in seconds for computing OHLC candles
        
    Returns:
        None
    """

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group="trade_to_ohlc",
        auto_offset_reset="earliest", # process all messages from the input topic when this service starts
    )
    
    # Input and output topics for the application
    input_topic = app.topic(name=kafka_input_topic, value_serializer="json")
    output_topic = app.topic(name=kafka_output_topic, value_serializer="json")

    # Create a streaming dataframe from the input topic
    sdf = app.dataframe(topic=input_topic)

    def init_ohlc_candle(value: dict) -> dict:
        """ 
        Initialize the OHLC candle with the first trade in the window

        Args:
            value (dict): Trade data

        Returns:    
            dict: OHLC candle data
        """

        return {
            "open": value["price"],
            "high": value["price"],
            "low": value["price"],
            "close": value["price"],
            "product_id": value["product_id"],
        }
  
    def update_ohlc_candle(ohlc_candle: dict, trade: dict) -> dict:
        """
        Update the OHLC candle with the new trade and return the updated candle

        Args:
            ohlc_candle (dict) : The current OHLC candle
            trade (dict) : The incoming trade
        
        Returns:
            dict : The updated OHLC candle
        
        """
        return { 
            "open": ohlc_candle["open"],
            "high": max(trade["price"], ohlc_candle["high"]),
            "low": min(trade["price"], ohlc_candle["low"]),
            "close": trade["price"],
            "product_id": ohlc_candle["product_id"],
        }

    # Aggregate trades into OHLC candles using tumbling windows
    sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
    sdf = sdf.reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle).current()
    
    # Extract the OHLC candle data
    sdf["open"] = sdf["value"]["open"]
    sdf["high"] = sdf["value"]["high"]
    sdf["low"] = sdf["value"]["low"]
    sdf["close"] = sdf["value"]["close"]
    sdf["product_id"] = sdf["value"]["product_id"]  

    # add timestamp
    sdf["timestamp"] = sdf["end"]

    # Keep only the required columns
    sdf = sdf[["timestamp", "product_id", "open", "high", "low", "close"]] 

    # Log the OHLC candles
    sdf = sdf.update(logger.info)

    # Write the OHLC candles to the output topic
    sdf = sdf.to_topic(output_topic)

    # Run the application
    app.run(sdf)

if __name__ == "__main__":
    trade_to_ohlc(
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_broker_address=config.kafka_broker_address,
        ohlc_window_seconds=config.ohlc_window_seconds,
    )