import json
import requests
from .finalized_class import Product
from .constants import EBAY_URL, satisfies_range
from .searcher_interface import SearcherInterface
from .custom_logger import log_class

@log_class
class EbaySearcher(SearcherInterface):
    
    def parse_json(self, product: str, min_value: float, max_value: float) -> dict:
       
        potential_data = self.send_request(product) 
        if potential_data:
            results = potential_data.get('results')
            finalized = []
            for product_instance in results:
                product_price = product_instance['price']
                product_name = product_instance['title']
                product_url = product_instance['url']

                if not satisfies_range(product_price, max_val = max_value, min_val = min_value):
                    continue
                finalized_product = Product(name = product_name, price = product_price, 
                                            product_url = product_url, site = 'Ebay')
                
                finalized.append(finalized_product.model_dump())
            return ('Ebay', finalized)
        
