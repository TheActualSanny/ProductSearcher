import logging

logger = logging.getLogger('__main__')
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream = logging.StreamHandler()
stream.setFormatter(format)
logger.addHandler(stream)

def log_method(method):
    '''
        This will be a decorator that will be used for logging.
        For not, this will be applied to the methods of searcher classes.
        Will probably be modified so that it will be a class decorator instead.
    '''
    def inner(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as err:
            exc_str = f'{method.__name__}:  Exception has been raised: {err}'
            logger.error(exc_str)
    return inner
