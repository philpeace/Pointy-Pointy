import sys
from Router import Router
from SessionManager import SessionManager
import cgi
from google.appengine.ext.webapp import template
import logging
import os
import traceback
import urlparse
from PeacePy.Web import Manager
from PeacePy.Configuration import Configuration

class Controller(object):
    def __init__(self, request, response):
        logging.info(request.path + ' ------------------------------------------------------------------------------------')
        self.request = request
        self.response = response
        self.sessionManager = SessionManager(self.request, self.response)
        self.session = self.sessionManager.current()
        self.action = ''
        self.name = ''
        self.items = {}
        self.initialize()
        logging.info(Configuration)

    def initialize(self):
        pass

    def handle_exception(self, e, debug):
        self.response.set_status(500)
        logging.exception(str(e))
        if debug:
            lines = ''.join(traceback.format_exception(* sys.exc_info()))
            self.response.clear()
            self.response.out.write('<pre>%s</pre>' % (cgi.escape(lines, quote=True)))

    def error(self, code):
        """Clears the response output stream and sets the given HTTP error code.

        Args:
          code: the HTTP status error code (e.g., 501)
        """
        self.response.set_status(code)
        self.response.clear()

    def rendertemplate(self, context=None, path=None):
        #try:
            if (path is None):
                path = '../views/%s/%s.html' % (self.name.lower(), self.action.lower())

            logging.debug('path = ' + path)

            if (context is None):
                context = dict()

            context['session'] = self.session
            context['request'] = self.request
            context['bodyClass'] = self.action
            context['router'] = Router()

            path = os.path.join(os.path.dirname(__file__), path)
            logging.debug(path)
            self.response.out.write(template.render(path, context))
        #except:
        #    self.transfer('Error', 'get', status='500')

    def redirect(self, uri, permanent=False):
        """Issues an HTTP redirect to the given relative URL.

        Args:
          uri: a relative or absolute URI (e.g., '../flowers.html')
          permanent: if true, we use a 301 redirect instead of a 302 redirect
        """
        
        try:
            logging.debug('Controller.redirect(' + uri + '), ' + str(permanent))

            if permanent:
                self.response.set_status(301)
            else:
                self.response.set_status(302)

            absolute_url = urlparse.urljoin(self.request.uri, uri)
            self.response.clear()
            self.response.headers['Location'] = str(absolute_url)
        except:
            self.transfer('Error', 'get', status='500')

    def transfer(self, controller, action, **kargs):
        """Transfers control to another Controller

        Args:
          controller: The module_name:class_name of the controller
          action: The name of the action
          kargs: Arguments to pass to the action
        """

        module_name, class_name = Manager.getModuleAndControllerNames(controller)

#        if controller.find(':') == -1:
#            module_name = 'controllers.%s' % controller
#            class_name = controller
#        else:
#            module_name, class_name = controller.split(':', 1)

        __import__(module_name)
        module = sys.modules[module_name]

        if (module is not None and hasattr(module, class_name)):
            c = getattr(module, class_name)(self.request, self.response)
        else:
            raise ImportError('Controller %s could not be initialized.' % (controller))

        if kargs is not None:
            getattr(c, action)(**kargs)
        else:
            getattr(c, action)()