import requests
import json
import os
from dotenv import load_dotenv
from .constants import AMAZON_URL
from .searcher_interface import SearcherInterface
from .custom_logger import log_class

@log_class
class AmazonSearcher(SearcherInterface):
    '''
        Class which is responsible for
        doing product lookups on amazon.
    '''
    def __init__(self, api_key: str, api_host: str):
        self._headers = {'x-rapidapi-key' : api_key, 'x-rapidapi-host' : api_host}

    def send_request(self, product: str) -> dict:
        '''
            Sends a request to the amazon endpoint and 
            fetches data for the product that the user searched for.
            Doesn't support pagination for now but will add it later.
        '''
        response = requests.get(AMAZON_URL, params = {'query' : product},
                                headers = self._headers)
        try:
            return response.json()    
        except requests.exceptions.JSONDecodeError:
            return None
    
    def parse_json(self, product: str, min_value: float, max_value: float) -> dict:
        '''
            Parses the products that were returned in send_request. 
            Will implement caching using redis so that redundant API calls 
            will be reduced.
        '''
        potential_data = self.send_request(product)
        if potential_data:
            products_data = potential_data.get('data').get('products')  
            finalized = []
            for product_instance in products_data:

                price = float(product_instance['product_price'][1:])
                if not self.satisfies_range(price, max_val = max_value, min_val = min_value):
                    continue
                
                product_name = product_instance['product_title']
                url = product_instance['product_url']

                finalized.append({'price' : price, 'name' : product_name,
                                  'site' : 'Amazon', 'product_url' : url})
            return ('Amazon', finalized)
        