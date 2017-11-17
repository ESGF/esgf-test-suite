import utils.globals as globals
import utils.authentication as auth

class AbstractMyproxyBasedTest(object):
  
  def __init__(self):
    if globals.myproxy_utils == None:
      globals.myproxy_utils = auth.MyProxyUtils()
      globals.myproxy_utils.get_trustroots()
      globals.myproxy_utils.get_credentials()