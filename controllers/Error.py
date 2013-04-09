from controllers.Controller import Controller as controllerBase
import logging

class Error(controllerBase):
    def get(self, status):
        logging.debug('Error.index ------------------()')

        context = {}
        context['status'] = status

        self.error(int(status))
        self.rendertemplate(context, path='../views/Error/' + str(status) + '.html')
