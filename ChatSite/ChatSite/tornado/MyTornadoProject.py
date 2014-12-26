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
   while not conn.is_closed:
      if not conn.stream.isConnected: # keep trying to connect to camera
         try:
            conn.stream.connect()
         except:
            conn.send( { 'image' : '' } )
            conn.send( { 'message' : 'Camera not connected' } )
      if conn.stream.isConnected:
         conn.send( { 'message' : 'Camera is connected' } )
         try:
            conn.send( { 'image' : base64.b64encode( conn.stream.getNextImage() ) } )
         except:
            print "conn.stream.getNextImage() failed"
            pass
      time.sleep( 1 )
      print "!"


class ImageWebSocket( SockJSConnection ):
   def on_open( self, request ):
      global myThread
      print "sockjs: open"
      self.stream = ImageStreamer.ImageStream( '192.168.1.133:8080' )
      if self.stream.isConnected:
         self.stream.close()
      myThread = threading.Thread( target=sendImage, args=( self, 1 ) )
      myThread.daemon = True
      myThread.start()

   def on_message( self, data ):
      print "data: %r" % ( data, )
      print data
      self.send(data)
      
   def on_close( self ):
      print "sockjs: close"

def ImageSockjsRouter( prefix ):
   return SockJSRouter( ImageWebSocket, prefix ).urls

