import requests
from dotenv import load_dotenv
from .custom_logger import log_class
from .searcher_interface import SearcherInterface
from .constants import ALIEXPRESS_URL

@log_class
class AliExpressSearcher(SearcherInterface):
    def __init__(self, api_key: str, api_host: str):
        self._headers = {'x-rapidapi-key' : api_key,
                         'x-rapidapi-host' : api_host}
          
    def send_request(self, product: str) -> dict:
        response = requests.get(ALIEXPRESS_URL, params = {'query' : product},
                                headers = self._headers)
        try:
            return response.json()
        except Exception as err:
            pass

    def parse_json(self, product: str, min_value: float, max_value: float) -> None:
        potential_data = self.send_request(product).get('data')
        finalized_data = []
        if not potential_data.get('note'):
            found_products = potential_data.get('content')
            for product in found_products:
                price_data = product.get('prices').get('salePrice')
                product_price = price_data.get('minPrice')
                if not self.satisfies_range(product_price, max_val = max_value, min_val = min_value):
                    continue
                product_url = product.get('store').get('storeUrl')
                product_name = product.get('title').get('displayTitle')
                finalized_data.append({'name' : product_name, 'price' : product_price,
                                       'url' : product_url, 'site' : 'Aliexpress'})
        return ('AliExpress', finalized_data)
