AMAZON_URL = "https://real-time-amazon-data.p.rapidapi.com/search"
EBAY_URL = 'https://ebay-search-result.p.rapidapi.com/search/{product}'
ALIEXPRESS_URL = 'https://aliexpress-data.p.rapidapi.com/product/search'

query_string = 'query'

def satisfies_range(product_price: float, min_val: float, max_val: float) -> tuple:
    '''
        The user must to have multiple options to pass a range, which means
        either only a minimum, only a maximum or a range or neither.
        This method accepts the passed values and a product instance,
        and it returns a boolean value.
    '''
    
    conditions = (not min_val and max_val and product_price <= max_val,
                not max_val and min_val and product_price >= min_val,
                max_val and min_val and min_val <= product_price <= max_val,
                not max_val and not min_val,)
    
    if any(conditions):
        return True