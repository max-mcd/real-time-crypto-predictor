import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebsocketTradeAPI:
    # https://docs.kraken.com/api/docs/websocket-v2/ohlc
    URL = 'wss://ws.kraken.com/v2'

    def __init__(
            self, 
            product_ids: List[str]
    ):
        self.product_ids = product_ids

        # Create a connection to the Kraken Websocket API
        self._ws = create_connection(self.URL)
        logger.info('Connected to Kraken Websocket API')

        # Subscribe to trades for the given product
        self.subscribe(product_ids=product_ids)

    def subscribe(self, product_ids: List[str]):
        """
        Subscribe to trades for the given product_ids.
        """
        logger.info(f'Subscribing to trades for {product_ids}')

        message = {
            'method': 'subscribe',
            'params': {
                'channel': 'trade', 
                'symbol': product_ids, 
                'snapshot': False,
            },
        }

        self._ws.send(json.dumps(message))
        logger.info('Subscribed to trades for {product_ids}')

        # For each of the product_its, 
        # ignore the first two messages since they only contain no trade data,
        # only subscription confirmation
        for product_id in product_ids:
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
        trades = [
            {
                'product_id': trade['symbol'],
                'price': trade['price'],
                'volume': trade['qty'],
                'timestamp': trade['timestamp'],
            } for trade in message['data']
        ]           

        breakpoint()
        return trades

    def is_done(self) -> bool:
        """
        The Websocket API is never done, so we keep fetching trades indefinitely.
        """
        return False
