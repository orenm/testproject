from django import template
register = template.Library()

TEMPLATE_PATH = 'converse/includes/'

@register.inclusion_tag( 'converse/static.html' )
def loadConversejs():
   return {}

@register.inclusion_tag( 'converse/init.html' )
def startConversejs():
   return {}

@register.inclusion_tag( 'converse/test.html' )
def show_test(xx):
   return {}

@register.simple_tag
def showConversejs():
    return "BLA"
