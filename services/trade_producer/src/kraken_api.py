import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebsocketTradeAPI:
    # https://docs.kraken.com/api/docs/websocket-v2/ohlc
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, product_id: str):
        self.product_id = product_id
        # Create a connection to the Kraken Websocket API
        self._ws = create_connection(self.URL)
        logger.info('Connected to Kraken Websocket API')

        # Subscribe to trades for the given product
        self.subscribe(product_id=product_id)

    def subscribe(self, product_id: str):
        """
        Subscribe to trades for the given product_id.
        """
        logger.info(f'Subscribing to trades for {product_id}')

        message = {
            'method': 'subscribe',
            'params': {'channel': 'trade', 'symbol': [product_id], 'snapshot': False},
        }

        self._ws.send(json.dumps(message))
        logger.info('Subscribed to trades')

        # ignore the first two messages since they only contain no trade data, only subscription confirmation
        _ = self._ws.recv()
        _ = self._ws.recv()

    def get_trades(self) -> List[Dict]:
        """
        Get trades from the Kraken Websocket API.
        """

        message = self._ws.recv()
        # if message contains '{'channel':'heartbeat'}' - ignore it
        if 'heartbeat' in message:
            return []

        # Parse the trade message
        message = json.loads(message)
        logger.info(f'Received message: {message}')

        # Parse all trades in the message and return them as a list of dictionaries
        trades = []
        for trade in message['data']:
            trades.append(
                {
                    'product_id': self.product_id,
                    'price': trade['price'],
                    'volume': trade['qty'],
                    'timestamp': trade['timestamp'],
                }
            )

        return trades
