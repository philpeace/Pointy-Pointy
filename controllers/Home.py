from PeacePy.Decorators import ActionBinder
from controllers.Controller import Controller as controllerBase
import logging

class Home(controllerBase):
    #@ActionBinder
    def index(self):
        logging.debug('Home.index ------------------()')

        self.rendertemplate()
