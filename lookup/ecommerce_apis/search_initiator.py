import os
from dotenv import load_dotenv
from .ebay import EbaySearcher
from .amazon import AmazonSearcher
from .aliexpress import AliExpressSearcher
from .search_manager import SearchManager
from .constants import ALIEXPRESS_URL, EBAY_URL, AMAZON_URL, query_string

load_dotenv()

def get_searcher(product: str) -> SearchManager:
    '''
        Initiates the search process and then returns
        a SearchManager instance, which will be re-used for lookups
        afterwards.
    '''

    api_key = os.getenv('API_KEY')
    amazon_manager = AmazonSearcher(api_key = api_key, api_host = os.getenv('AMAZON_HOST'),
                                    url = AMAZON_URL, query_word = query_string)
    ebay_manager = EbaySearcher(api_key = api_key, api_host = os.getenv('EBAY_HOST'),
                                url = EBAY_URL.format(product = product), query_word = None)
    alixpress_manager = AliExpressSearcher(api_key = api_key, api_host = os.getenv('ALIEXPRESS_HOST'),
                                           url = ALIEXPRESS_URL, query_word = query_string)
    searcher = SearchManager(amazon_manager, ebay_manager, alixpress_manager)
    return searcher
