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


import ImageStreamer
import base64
import threading
import time


myThread = None

def sendImage( conn, delay ):
   while conn.stream.isConnected and not conn.is_closed:
      print "!"
      conn.send( { 'image' : base64.b64encode( conn.stream.getNextImage() ) } )
      time.sleep( 1 )

class ImageWebSocket( SockJSConnection ):
   def on_open( self, request ):
      global myThread
      print "sockjs: open"
      self.stream = ImageStreamer.ImageStream( '192.168.1.133:8080' )
      if self.stream.isConnected:
         self.stream.close()
      self.stream.connect()
      message = u'Connected to camera' if self.stream.isConnected else u'Camera not ready'
         
      myThread = threading.Thread( target=sendImage, args=( self, 1 ) )
      myThread.daemon = True
      myThread.start()
#      self.send( message )
#      self.send( { 'image' : 'no' } )
#      self.send( { 'image' : base64.b64encode( self.stream.getNextImage() ) } )

   def on_message( self, data ):
      print "data: %r" % ( data, )
      print data
      self.send(data)
      
   def on_close( self ):
      print "sockjs: close"

def ImageSockjsRouter( prefix ):
   return SockJSRouter( ImageWebSocket, prefix ).urls

