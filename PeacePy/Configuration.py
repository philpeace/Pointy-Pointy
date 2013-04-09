import logging

class Configuration(object):
    def __init__(self):
        logging.debug('Configuration(__init__)')
        self.ViewPath = '/views'
        self.ErrorController = 'Error'

    def __str__(self):
        return '{' + self.ViewPath +  ' ' + self.ErrorController + '}'