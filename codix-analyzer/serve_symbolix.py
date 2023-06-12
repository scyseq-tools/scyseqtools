from .ladon.server.wsgi import LadonWSGIApplication
import wsgiref.simple_server

# if after __name__ == '__main__'
# that serves 2 intances of symbolic see ladon/server/wsgi_application
# method import_services
# thus we make a separate file ...
application = LadonWSGIApplication(['symbolix'],['.'])

server = wsgiref.simple_server.make_server('', 8081, application)
server.serve_forever()

