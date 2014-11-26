from django import template
register = template.Library()

TEMPLATE_PATH = 'converse/includes/'


@register.inclusion_tag( 'converse/static.html' )
def loadConversejs():
   return {}

@register.inclusion_tag( 'converse/init.html', takes_context=True )
def startConversejs( context ):
   return get_conversejs_context( context )

@register.inclusion_tag( 'converse/test.html' )
def show_test(xx):
   return {}

@register.simple_tag
def showConversejs():
    return "BLA"

from .. import conf
from .. import boshclient

def get_conversejs_context( context ):
   if not conf.CONVERSEJS_ENABLED:
      return context

   context.update( conf.get_conversejs_settings() )
   request = context.get( 'request' )

   jid_domain = conf.CONVERSEJS_AUTO_REGISTER
   #jid = request.user.username + u'@' + jid_domain
   jid = 'kuku' + u'@' + jid_domain
   password = 'balabush'

   bosh = boshclient.BOSHClient( jid, password, context[ 'CONVERSEJS_BOSH_SERVICE_URL' ] )
   jid, sid, rid = bosh.get_credentials()
   bosh.close_connection()

   context.update( { 'jid': jid, 'sid': sid, 'rid': rid } )
   print { 'jid': jid, 'sid': sid, 'rid': rid }
   return context
