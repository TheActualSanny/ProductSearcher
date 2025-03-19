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

    def parse_product(self, product: dict, min_value: float, max_value: float):
            price = float(product['product_price'][1:])
            if satisfies_range(price, max_val = max_value, min_val = min_value):
                product_name = product['product_title']
                url = product['product_url']
                return Product(name = product_name, price = price,
                               product_url = url, site = 'Amazon')

    def parse_json(self, product: str, min_value: float, max_value: float) -> tuple:
        '''
            Parses the products that were returned in send_request. 
            Will implement caching using redis so that redundant API calls 
            will be reduced.
        '''
        finalized = super().parse_json(product, min_value = min_value, max_value = max_value)
        return ('Amazon', finalized)
        