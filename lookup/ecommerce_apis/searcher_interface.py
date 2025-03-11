from abc import ABCMeta, abstractmethod

class SearcherInterface:
    '''
        Provides an interface for the
        searcher classes. Essentially, the main important
        methods are send_request and parse_json
    '''

    def send_request(self, product: str):
        pass

    def parse_json(self, product: str):
        pass