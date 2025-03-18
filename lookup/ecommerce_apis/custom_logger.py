import logging
import functools
import requests 

logger = logging.getLogger('__main__')
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream = logging.StreamHandler()
stream.setFormatter(format)
logger.addHandler(stream)


def log_method(cls_name):
    '''
        We have an outer function wrapping the decorator.
        This is done in order to access the class name, so that
        in the case of an exception, we know which searcher class raised it and which method.     
    '''
    def outer(method):
        @functools.wraps(method)
        def inner(*args, **kwargs):
            log_str = f'{cls_name} - {method.__name__}: ' + '{message}'
            try:
                result = method(*args, **kwargs)
                logger.info(f'{log_str.format(message = result)}')
                return result
            except ValueError as ex:
                logger.error(log_str.format(message = f'ValueError raised: {ex}'))
            except requests.JSONDecodeError as ex:
                logger.error(log_str.format(message = f'Failed to decode the JSON result: {ex}'))
        return inner
    return outer

# TODO: Multiple exception blocks
# Pydantic
def log_class(cls):
    class ModifiedClass:
        def __init__(self, *args, **kwargs):
            self.oInstance = cls(*args, **kwargs)
        def __getattribute__(self, attr):
            try:
                x = super(ModifiedClass, self).__getattribute__(attr)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(attr)
            if type(x) == type(self.__init__):
                return log_method(self.oInstance.__class__)(x)
            else:
                return x
    return ModifiedClass
