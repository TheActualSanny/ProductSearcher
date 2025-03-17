import requests
import json
import os
from dotenv import load_dotenv
from .finalized_class import Product
from .constants import AMAZON_URL, satisfies_range
from .searcher_interface import SearcherInterface
from .custom_logger import log_class

@log_class
class AmazonSearcher(SearcherInterface):
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
                if not satisfies_range(price, max_val = max_value, min_val = min_value):
                    continue
                product_name = product_instance['product_title']
                url = product_instance['product_url']
                finalized_product = Product(name = product_name, price = price,
                                            product_url = url, site = 'Amazon')
                finalized.append(finalized_product.model_dump())
            return ('Amazon', finalized)
        