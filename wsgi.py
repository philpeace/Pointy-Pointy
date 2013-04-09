import sys

from google.appengine.ext.webapp import Request
from google.appengine.ext.webapp import Response
import logging
import middlewareConfig
from PeacePy.Configuration import Configuration
from PeacePy.Web import Manager

class WSGIApplication(object):
    """Wraps a set of webapp RequestHandlers in a WSGI-compatible application.
    This is based on webapp's WSGIApplication by Google, but uses Routes library
    (http://routes.groovie.org/) to match url's.
    """
    def __init__(self, mapper, debug=False):
        """Initializes this application with the given URL mapping.
        Args:
          mapper: a routes.mapper.Mapper instance
          debug: if true, we send Python stack traces to the browser on errors
        """
        self.mapper = mapper
        self.__debug = debug
        WSGIApplication.active_instance = self
        self.current_request_args = ()

    def __call__(self, environ, start_response):
        """Called by WSGI when a request comes in."""
        request = Request(environ)
        response = Response()
        WSGIApplication.active_instance = self
        # Match the path against registered routes.
        kargs = self.mapper.match(request.path)

        logging.critical('request.path = '+str(request.path))
        logging.critical('initial kargs = '+str(kargs))

        try:
            if kargs is None or 'controller' not in kargs:
                logging.debug('kargs is None')
                kargs = dict(controller='Error', status='404')

            module_name, class_name = Manager.getModuleAndControllerNames(kargs['controller'])

            del kargs['controller']

            logging.debug('module_name = ' + module_name)
            logging.debug('class_name = ' + class_name)
        except Exception, e:
            logging.debug('CRITICAL: ' + str(e))
            raise TypeError('Controller is not set, or not formatted in the form "my.module.name:MyControllerName".' + str(e))

        # Initialize matched controller from given module.
        __import__(module_name)
        module = sys.modules[module_name]

        if (module is not None and hasattr(module, class_name)):
            controller = getattr(module, class_name)(request, response)
        else:
            raise ImportError('Controller %s could not be initialized.' % (class_name))

        # Use the action set in the route, or the HTTP method.
        if kargs is not None and 'action' in kargs:
            action = kargs['action']
            del kargs['action']
        else:
            action = environ['REQUEST_METHOD'].lower()
            if action not in ['get', 'post', 'head', 'options', 'put', 'delete', 'trace']:
                action = None

        if controller:
            mwProceed = True

            if len(middlewareConfig.middlewareClasses) > 0:
                logging.critical('middlewareConfig.middlewareClasses = ' + str(middlewareConfig.middlewareClasses))
#                for mw in middlewareConfig.middlewareClasses:
#                logging.critical('mw = ' + str(mw))
                mwModuleName, mwClassName = middlewareConfig.middlewareClasses.split(':', 1)

                logging.critical('mwModuleName = ' + mwModuleName)
                logging.critical('mwClassName = ' + mwClassName)

                __import__(mwModuleName)
                wmModule = sys.modules[mwModuleName]

                if (wmModule and hasattr(wmModule, mwClassName)):
                    mwClass = getattr(wmModule, mwClassName)()
                    mwProceed = mwProceed and mwClass.processRequest(controller)

#                    if not mwProceed:
#                        break

            logging.critical('mwProceed = ' + str(mwProceed))
            logging.critical('controller = ' + str(controller))
            logging.critical('action = ' + str(action))
            logging.critical('kargs = ' + str(kargs))

            if mwProceed and action:
                try:
                    # Execute the requested action, passing the route dictionary as
                    # named parameters.
                    controller.action = action
                    controller.name = class_name

                    if kargs is not None:
                        getattr(controller, action)(** kargs)
                    else:
                        getattr(controller, action)()
                except Exception, inst:
                    controller.handle_exception(inst, self.__debug)

            response.wsgi_write(start_response)
            return ['']
        else:
            response.set_status(404)
