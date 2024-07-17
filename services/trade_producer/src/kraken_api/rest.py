from typing import Dict, List
import json
import requests
from loguru import logger

class KrakenRestAPI: 
    # https://docs.kraken.com/api/docs/rest-api/get-recent-trades/
    URL = "https://api.kraken.com/0/public/Trades?pair={product_id}&since={since_sec}"

    def __init__(
              self,
              product_ids: List[str],
              from_ms: int,
              to_ms: int,
    ) -> None:
        """
        Initialize the Kraken REST API client.
        
        Args:
            product_ids (List[str]): A list of product IDs for which to fetch trades.
            from_ms (int): The start of the time range in milliseconds.
            to_ms (int): The end of the time range in milliseconds
        
        Returns:
            None
        """
        self.product_ids = product_ids
        self.from_ms = from_ms
        self.to_ms = to_ms

        # If we're done fetching historical data, the last batch of trades has 
        # a data['result'][product_id]['last'] >= self.to_ms
        self._is_done = False        
        
    def get_trades(self) -> List[Dict]:
        """
        Get a batch trades from the Kraken REST API and returns them as 
        a list of dictionaries.

        Args:
            None

        Returns:
            List[Dict]: A list of trades as dictionaries.
        """
        payload = {}
        headers = {'Accept': 'application/json'}

        # replacing the placeholders in the URL with the actual values for
        # - product_id
        # - since_sec
        since_sec = self.from_ms // 1000
        url = self.URL.format(product_id=self.product_ids[0], since_sec=since_sec)

        response = requests.request("GET", url, headers=headers, data=payload)

        # Parse the response into a JSON object
        data = json.loads(response.text)

        # TODO: Handle errors           
        # if data['error']:
        #     raise Exception(response['error'])
        
        trades = [
            {
                'price': trade[0],
                'volume': trade[1],
                'time': trade[2],
                'product_id': self.product_ids[0],
            } for trade in data['result'][self.product_ids[0]]
        ]
        
        # Check if we're done fetching historical data
        last_ts_in_ns =  int(data['result']['last'])

        # Convert the last timestamp to milliseconds
        last_ts_in_ms = last_ts_in_ns // 1000

        # If the last timestamp is greater than or equal to the end of the 
        # time range, we're done
        if last_ts_in_ms >= self.to_ms:
            self._is_done = True

        logger.debug(f'Fetched {len(trades)} trades')
        # log the last trade timestamp
        logger.debug(f'Last trade timestamp: {last_ts_in_ms}')

        breakpoint()

        return trades        

    def is_done(self) -> bool:
        """
        Check if all trades have been fetched.
        """
        return self._is_done