import os
from dotenv import load_dotenv
from .ebay import EbaySearcher
from .amazon import AmazonSearcher
from .aliexpress import AliExpressSearcher
from .search_manager import SearchManager

load_dotenv()

def get_searcher() -> SearchManager:
    '''
        Initiates the search process and then returns
        a SearchManager instance, which will be re-used for lookups
        afterwards.
    '''
    api_key = os.getenv('API_KEY')
    amazon_manager = AmazonSearcher(api_key = api_key, api_host = os.getenv('AMAZON_HOST'))
    ebay_manager = EbaySearcher(api_key = api_key, api_host = os.getenv('EBAY_HOST'))
    alixpress_manager = AliExpressSearcher(api_key = api_key, api_host = os.getenv('ALIEXPRESS_HOST'))
    searcher = SearchManager(amazon_manager, ebay_manager, alixpress_manager)
    return searcher
