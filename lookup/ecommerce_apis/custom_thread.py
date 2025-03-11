from threading import Thread

class ManagerThread(Thread):
    '''
        We extend the Thread class in order to
        add a return method so that we can retrieve
        the data that a thread instance returns.
    '''

    def __init__(self, name = None, target = None, group = None, 
                 args = (), kwargs = {}, verbose = None):
        super().__init__(group, target, name, args, kwargs)
        self._return_value = None

    def run(self):
        if not self._return_value:
            self._return_value = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return_value
