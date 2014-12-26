#!/usr/bin/env python
# All rights reserved.
# Confidential and Proprietary.

from tornado.options import options, define
import django.core.handlers.wsgi
import tornado.httpserver, tornado.ioloop
import tornado.web, tornado.wsgi
import MyTornadoProject


import os, sys
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = 'ChatSite.settings'
sys.path.append( os.path.expanduser( '/home/oren/src/testproject/ChatSite' ) )

import django
django.setup()

#portNumber, sslPortNumber = ( 8000, 8001 )
portNumber, sslPortNumber = ( 80, 443 )

define( 'port', type=int, default=portNumber )
define( 'sslport', type=int, default=sslPortNumber )

settingsWithSsl = dict()

settingsWithSsl[ 'ssl_options' ] = { 
   "certfile": os.path.join( "/etc/pki/tls/certs/ssl.crt" ),
   "keyfile": os.path.join( "/etc/pki/tls/private/ssl.key" ),
   }

wsgi_app = tornado.wsgi.WSGIContainer(
   django.core.handlers.wsgi.WSGIHandler() )

class HelloHandler( tornado.web.RequestHandler ):
  def get(self):
    self.write('Hello from tornado')

templatesPath = os.path.join( os.path.dirname( __file__ ), 'templates' )

# /echo1/index.html for page example. "/echo" is for the websocket
tornado_app = tornado.web.Application(
   MyTornadoProject.EchoSockjsRouter( '/echo' ) +
   MyTornadoProject.ImageSockjsRouter( '/vid' ) + 
   [ ( '/hello-tornado', HelloHandler ),
     ( r'/vid/(.*)', tornado.web.StaticFileHandler, { 'path': templatesPath } ),
#     ( r'/echo1/(.*)', tornado.web.StaticFileHandler, { 'path': templatesPath } ),
     ( r'/static/(.*)', tornado.web.StaticFileHandler, { 'path': '/var/www/chat/static' } ),
     ( '.*', tornado.web.FallbackHandler, dict( fallback=wsgi_app ) ),
     ], debug=True )

if hasattr( options, 'sslport' ):
   server = tornado.httpserver.HTTPServer( tornado_app, **settingsWithSsl )
   server.listen( options.sslport )
   # is sslport defined, redirect port to sslport 
   class MyRedirectHandler( tornado.web.RequestHandler ):
      def get( self, path ):
         self.redirect(
            'https://' + self.request.host.split( ':' )[ 0 ] + ':' + \
               str( options.sslport ) + self.request.uri, permanent=True )
   redirect_app = tornado.web.Application( [ ( r'/(.*)', MyRedirectHandler ) ] )
   redirectServer = tornado.httpserver.HTTPServer( redirect_app )
   redirectServer.listen( options.port )
else:
   server = tornado.httpserver.HTTPServer( tornado_app )
   server.listen( options.port )
   

print "[*] Listening at 0.0.0.0:%i" % ( options.port, )
tornado.ioloop.IOLoop.instance().start()
