from PeacePy.Decorators import ActionBinder
from controllers.Controller import Controller as controllerBase
from google.appengine.api import channel
import logging

class Home(controllerBase):
    #@ActionBinder
    def index(self):
        logging.info('Home.index ------------------()')
        token = channel.create_channel('foo')
        logging.info('token = ' + token)
        c = {}
        c['token'] = token
        self.rendertemplate(context=c)
