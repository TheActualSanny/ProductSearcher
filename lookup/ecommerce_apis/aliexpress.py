import requests
from dotenv import load_dotenv
from .finalized_class import Product
from .custom_logger import log_class
from .searcher_interface import SearcherInterface
from .constants import ALIEXPRESS_URL, satisfies_range

@log_class
class AliExpressSearcher(SearcherInterface):

    def parse_product(self, product: dict, min_value: float, max_value: float):
        print(product)
        price_data = product.get('prices').get('salePrice')
        product_price = price_data.get('minPrice')
        if satisfies_range(product_price, max_val = max_value, min_val = min_value):
            product_url = product.get('store').get('storeUrl')
            product_name = product.get('title').get('displayTitle')
            return Product(name = product_name, product_url = product_url,
                           site = 'Aliexpress', price = product_price)
        
    def parse_json(self, product: str, min_value: float, max_value: float) -> tuple:
        finalized = super().parse_json(product, min_value = min_value, max_value = max_value)
        return ('AliExpress', finalized)
