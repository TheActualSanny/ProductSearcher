import requests
from dotenv import load_dotenv
from .finalized_class import Product
from .custom_logger import log_class
from .searcher_interface import SearcherInterface
from .constants import ALIEXPRESS_URL, satisfies_range

@log_class
class AliExpressSearcher(SearcherInterface):
    
    def parse_json(self, product: str, min_value: float, max_value: float) -> None:
        potential_data = self.send_request(product).get('data')
        finalized_data = []
        if not potential_data.get('note'):
            found_products = potential_data.get('content')
            for product_instance in found_products:
                price_data = product_instance.get('prices').get('salePrice')
                product_price = price_data.get('minPrice')
                if not satisfies_range(product_price, max_val = max_value, min_val = min_value):
                    continue
                product_url = product_instance.get('store').get('storeUrl')
                product_name = product_instance.get('title').get('displayTitle')
                finalized_product = Product(name = product_name, product_url = product_url,
                                            site = 'Aliexpress', price = product_price)
                finalized_data.append(finalized_product.model_dump())
        return ('AliExpress', finalized_data)
