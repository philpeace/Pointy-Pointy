from controllers.Controller import Controller as controllerBase
from models.Map import Map as MapModel
import PeacePy
import logging

class Map(controllerBase):
    @Decorators.ActionBinder
    def view(self, id):
        logging.debug('Map.view ------------------()')

        self.rendertemplate()

    @Decorators.ActionBinder
    def create(self, name, description):
        logging.debug('Map.create ------------------()')

        raise Error('Foo')

        m = MapModel(name=name, description=description)
        m.put()
        self.rendertemplate()

    @Decorators.ActionBinder
    def new(self):
        logging.debug('Map.new ------------------()')


        self.rendertemplate()

    @Decorators.ActionBinder
    def list(self):
        logging.debug('Map.list ------------------()')

        c = {}
        c['maps'] = MapModel.all()

        self.rendertemplate(context=c)
