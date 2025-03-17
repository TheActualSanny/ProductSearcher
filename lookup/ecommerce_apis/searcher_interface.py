import requests

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
        params = None if not self._query_word else {self._query_word : product}
        response = requests.get(self._url, headers = self._headers, 
                                params = params)
        try:
            return response.json()
        except requests.JSONDecodeError:
            return 
    
    def parse_json(self, product: str):
        data = self.send_request(product = product,
                                 url = self._url)
        