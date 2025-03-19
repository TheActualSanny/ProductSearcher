import json
import requests
from .finalized_class import Product
from .constants import EBAY_URL, satisfies_range
from .searcher_interface import SearcherInterface
from .custom_logger import log_class

@log_class
class EbaySearcher(SearcherInterface):
    
    def parse_product(self, product: dict, min_value: float, max_value: float):

        product_price = product['price']
        product_name = product['title']
        product_url = product['url']
        if satisfies_range(product_price, max_val = max_value, min_val = min_value):
            return Product(name = product_name, price = product_price, 
                           product_url = product_url, site = 'Ebay')

    def parse_json(self, product: str, min_value: float, max_value: float) -> tuple:
        finalized = super().parse_json(product, min_value = min_value, max_value = max_value) 
        return ('Ebay', finalized)
        
