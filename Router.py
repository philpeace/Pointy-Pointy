import logging
from routes.util import url_for

class Router(object):
    def __init__(self):
        logging.debug('Router __init__')

    def __get__(self, name):
        logging.debug('Router __get__')
        url = url_for(name)
        logging.debug('Router[' + name + '] = ' + str(url))
        return url

    def __getattr__(self, name):
        logging.debug('Router __getattr__')
        url = url_for(name)
        logging.debug('Router[' + name + '] = ' + str(url))
        return url