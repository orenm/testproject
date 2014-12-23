#!/usr/bin/env python
# All rights reserved.
# Confidential and Proprietary.

from sockjs.tornado import SockJSRouter, SockJSConnection

class EchoWebSocket( SockJSConnection ):
  def on_open( self, request ):
      print "sockjs: open"

  def on_message( self, data ):
      print "data: %r" % ( data, )
      self.send(data)

  def on_comment( self, data ):
      print "data: %r" % ( data, )
      self.send( data )

  def on_close( self ):
      print "sockjs: close"

def EchoSockjsRouter( prefix ):
    return SockJSRouter( EchoWebSocket, prefix ).urls
