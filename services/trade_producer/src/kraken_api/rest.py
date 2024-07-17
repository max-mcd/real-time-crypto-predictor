from typing import Dict, List
import requests

class KrakenRestAPI: 
    # https://docs.kraken.com/api/docs/rest-api/get-recent-trades/
    URL = "https://api.kraken.com/0/public/Trades?pair={product_id}&since={since_ms}"

    def __init__(
              self,
              product_ids: List[str],
              from_ms: int,
    ) -> None:
        """
        Initialize the Kraken REST API client.
        
        Args:
            product_ids (List[str]): A list of product IDs for which to fetch trades.
            from_ms (int): The start of the time range in milliseconds.
        
        Returns:
            None
        """
        self.product_ids = product_ids
        self.from_ms = from_ms
        
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
        # - since_ms
        url = self.URL.format(product_id=self.product_ids[0], since_ms=self.from_ms)
        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        import json
        data = json.loads(response.text)
        breakpoint()

    def is_done(self) -> bool:
        """
        Check if all trades have been fetched.
        """
        return False