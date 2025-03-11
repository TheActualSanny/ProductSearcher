import json
import requests
from .constants import EBAY_URL
from .searcher_interface import SearcherInterface
class EbaySearcher(SearcherInterface):

    def __init__(self, api_key: str, api_host: str):
        self._headers = {'x-rapidapi-key' : api_key,
                        'x-rapidapi-host' : api_host}
    
    def send_request(self, product: str) -> dict:
        response = requests.get(EBAY_URL.format(product = product), headers = self._headers, 
                                params = {'keyword' : product})
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return

    def parse_json(self, product: str) -> dict:
        potential_data = self.send_request(product)
        
        if potential_data:
            results = potential_data.get('results')
            finalized = []
            for product_instance in results:

                product_name = product_instance['title']
                product_price = product_instance['price']
                product_url = product_instance['url']
                finalized.append({'name' : product_name, 'site' : 'Ebay', 'price' : product_price,
                                  'product_url' : product_url})
                
            print('Successfully fetched ebay data!')
            return ('Ebay', finalized)
        
