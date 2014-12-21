#!/usr/bin/env python
# All rights reserved.
# Confidential and Proprietary.

import httplib
import re
import threading
import select

class ImageStream( object ):
   chunkSize = 100
   def __init__( self, serverName ):
      self.conn = httplib.HTTPConnection( serverName )
      self._buf = ''
      self.lock = threading.Lock()

   @property
   def isConnected( self ):
      return self.conn.sock != None

   def connect( self ):
      self.conn.connect()
      self.conn.sock.setblocking( 0 )

   def readChunk( self, count, timeout=3 ):
      ready = select.select( [ self.conn.sock ], [], [], timeout )
      string = ''
      if ready[ 0 ]:
         string = self.conn.sock.recv( count )
      if len( string ) == 0 or not ready[ 0 ]:
         self.conn.close()
         self._buf = ''
         raise EOFError
      return string

   def waitForString( self, string='Content-Length: ' ):
      index = -1
      prevBuf = ''
      while index < 0:
         buf = self.readChunk( self.chunkSize )
         bothBufs = prevBuf + buf
         prevBuf = buf
         index = bothBufs.find( string )
         print "[waitForString]", len( buf )
      self._buf = bothBufs[ index : ] + self.readChunk( self.chunkSize )

   def getContentLength( self ):
      self.waitForString( 'Content-Length: ' )
      match = re.search( 'Content-Length: (\d+)\r\n', stream._buf )
      if match:
         return int( match.groups()[ 0 ] )
      else:
         return None


   def getNextImage( self ):
      with self.lock:
         # clear buffer:
         import time;time.sleep(.1) # why a sleep here is important?
         xx = self.readChunk( 1000000, 0 )
         ##print "xx", len(xx)
         print "-"* 50
         length = self.getContentLength()
         while len( self._buf ) < length:
            block = self.readChunk( length - len( self._buf ) )
            print "readBlock", length, len( self._buf ), len( block )
            self._buf += block
         imageOffset = self._buf.find( '\r\n\r\n' )
         return self._buf[ imageOffset + 4:]
      

stream = ImageStream( '192.168.1.133:8080' )

