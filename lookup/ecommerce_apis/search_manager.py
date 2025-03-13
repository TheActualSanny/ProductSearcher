import json
from .custom_thread import ManagerThread

class SearchManager:

    def __init__(self, *searchers):
        '''
            The actual search managers are inserted into a list,
            so there is no need to modify the code once new searchers 
            will be implemented.
        '''

        self.managers = []
        for searcher in searchers:
            self.managers.append(searcher)

    def start_searching(self, product_input: str, min_value: int, max_value: int) -> None:
        '''
            The target product is passed to this method, which will then
            call each one of the manager's parse_json methods, respectively.
        '''
        finalized_data = dict()
        threads = [ManagerThread(target = searcher.parse_json, args = (product_input, min_value, max_value)) 
                   for searcher in self.managers]

        for thread in threads:
            thread.start()
        
        for thread in threads:
            searcher_result = thread.join()
            if searcher_result:
                finalized_data[searcher_result[0]] = searcher_result[1]
        return finalized_data
