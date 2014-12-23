#!/usr/bin/env python
# All rights reserved.
# Confidential and Proprietary.

from tornado.options import options, define
import django.core.handlers.wsgi
import tornado.httpserver, tornado.ioloop
import tornado.web, tornado.wsgi
#import MyTornadoProject


import os, sys
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = 'ChatSite.settings'
sys.path.append( os.path.expanduser( '~/src/testproject/ChatSite' ) )

import django
django.setup()

define( 'port', type=int, default=8000 )

wsgi_app = tornado.wsgi.WSGIContainer(
   django.core.handlers.wsgi.WSGIHandler() )

class HelloHandler( tornado.web.RequestHandler ):
  def get(self):
    self.write('Hello from tornado')


tornado_app = tornado.web.Application(
#    MyTornadoProject.EchoSockjsRouter( '/echo' ) + [
   [  ( '/hello-tornado', HelloHandler ),
      ( r'/static/(.*)', tornado.web.StaticFileHandler, { 'path': '/var/www/chat/static' } ),
      ( '.*', tornado.web.FallbackHandler, dict( fallback=wsgi_app ) ),
      ] )

server = tornado.httpserver.HTTPServer( tornado_app )
server.listen( options.port )
print "[*] Listening at 0.0.0.0:%i" % ( options.port, )
tornado.ioloop.IOLoop.instance().start()
