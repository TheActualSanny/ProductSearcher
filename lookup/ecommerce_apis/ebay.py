import json
import requests
from .constants import EBAY_URL
from .searcher_interface import SearcherInterface
from .custom_logger import log_method
class EbaySearcher(SearcherInterface):

    def __init__(self, api_key: str, api_host: str):
        self._headers = {'x-rapidapi-key' : api_key,
                        'x-rapidapi-host' : api_host}
    
    @log_method
    def send_request(self, product: str) -> dict:
        response = requests.get(EBAY_URL.format(product = product), headers = self._headers, 
                                params = {'keyword' : product})
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return
        
    @log_method
    def parse_json(self, product: str, min_value: float, max_value: float) -> dict:
        potential_data = self.send_request(product)
        
        if potential_data:
            results = potential_data.get('results')
            finalized = []
            for product_instance in results:
                product_price = None
                try:
                    product_price = float(product_instance['price'][1:])
                except:
                    partitioned = product_instance['price'].split()
                    product_price = float(''.join(partitioned[0][1:].split(',')))
                if not self.satisfies_range(product_price, max_val = max_value, min_val = min_value):
                    continue
                product_name = product_instance['title']
                product_url = product_instance['url']
                finalized.append({'name' : product_name, 'site' : 'Ebay', 'price' : product_price,
                                  'product_url' : product_url})
            return ('Ebay', finalized)
        
