from google.appengine.ext.webapp.util import run_wsgi_app
import webapp2
from routes.mapper import Mapper
from routing import add_routes
from wsgi import WSGIApplication
import logging

map = Mapper()
add_routes(map)

logging.getLogger().setLevel(logging.INFO)

app = WSGIApplication(map, debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()