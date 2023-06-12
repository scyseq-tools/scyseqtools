import threading
from .ladon.server.wsgi import LadonWSGIApplication
import wsgiref.simple_server

from .analix import Application

# if after __name__ == '__main__'
# that serves 2 intances of symbolic see ladon/server/wsgi_application
# method import_services
# thus we make a separate file ...

class ServerThread(threading.Thread):

    def run(self):
        application = LadonWSGIApplication(['symbolix'],['./server'])

        server = wsgiref.simple_server.make_server('', 8081, application)
        server.serve_forever()

class ClientThread(threading.Thread):

    def run(self):
        application = Application()
        application.mainloop()

server = ServerThread()
server.daemon = True
server.start()
client = ClientThread()
client.start()
