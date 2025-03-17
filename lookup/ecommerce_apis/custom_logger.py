import logging
import functools

logger = logging.getLogger('__main__')
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream = logging.StreamHandler()
stream.setFormatter(format)
logger.addHandler(stream)


def log_method(method):
    '''
        This will be a decorator that will be used for logging.
        For now. A seperate decorator will be written for the searcher classes
        which will wrap every method with log_method.
    '''
    @functools.wraps(method)
    def inner(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as ex:
            exc_str = f'{method.__doc__}:  Exception has been raised: {ex}'
            logger.error(exc_str)
    return inner

# MUSTADD: Multiple exception blocks
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
                return log_method(x)
            else:
                return x
    return ModifiedClass
