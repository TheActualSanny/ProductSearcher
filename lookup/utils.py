import json 
from django.core.cache import cache

def set_cache(*lookup_args,  products: tuple):
    '''
        The TTL for the cache will be 5 minutes.
        The actual redis key is going to be a JSON string, so that
        later on we can compare not only the products, but the price ranges.
    '''
    new_key = json.dumps(lookup_args)
    cache.set(new_key, products, timeout = 300)

def get_cache(*lookup_args) -> dict:
    '''
        Will serialize the passed tuple as a JSON string and will
        check if there is a value associated with it.
    '''
    jsonified_args = json.dumps(lookup_args)
    data = cache.get(jsonified_args) 
    return data