import requests
from abc import ABC, abstractmethod
from .finalized_class import Product

class SearcherInterface:
    '''
        Provides an interface for the
        searcher classes. Essentially, the main important
        methods are send_request and parse_json
    '''

    def __init__(self, api_key: str, api_host: str, url: str,
                 query_word: str = None):
        self._query_word = query_word
        self._headers = {'x-rapidapi-key' : api_key,
                         'x-rapidapi-host' : api_host}
        self._url = url

    def send_request(self, product: str) -> dict:
        '''
            Sends a request to the API and fetches the data.
        '''
        params = None if not self._query_word else {self._query_word : product}
        response = requests.get(self._url, headers = self._headers, 
                                params = params)
        try:
            return response.json()
        except requests.JSONDecodeError:
            return 
    
  
    def parse_product(self, product: dict, min_value: float,
                      max_value: float) -> Product:
        '''
            Each searcher class will have it's specific implementation.
        '''
        pass


    def parse_json(self, product: str, min_value: float, max_value: float) -> tuple:
        '''
            Parses the data that is fetched by send_request. 
        '''
        data = self.send_request(product = product)
        finalized_data = []
        try:
            ebay_data = data.get('data').get('products')
        except AttributeError:
            ebay_data = None

        try:
            aliexpress_data = data.get('data').get('content')
        except AttributeError:
            aliexpress_data = None
        # TODO: The keys for seperate searchers will probably be stored as class attributes
        dict_variants = (data.get('results'), aliexpress_data,
                         ebay_data)
        for i in dict_variants:
            if i:
                data = i
                break

        for product_instance in data:
            finalized_data.append(
                self.parse_product(product_instance, min_value = min_value,
                                   max_value = max_value).model_dump()
            )

        return finalized_data
