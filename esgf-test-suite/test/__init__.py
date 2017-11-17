import utils.globals as globals
import utils.naming as naming

def teardown_package():
  
  if globals.browser != None and not naming.IS_DEBUG:
    globals.browser.quit()
  
  if globals.myproxy_utils != None and not naming.IS_DEBUG:
    globals.myproxy_utils.delete_credentials()
    globals.myproxy_utils.delete_trustroots()