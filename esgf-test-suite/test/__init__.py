import utils.globals as globals

def teardown_package():
  
  if globals.browser != None and not globals.is_debug:
    globals.browser.quit()
  
  if globals.myproxy_utils != None and not globals.is_debug:
    globals.myproxy_utils.delete_credentials()
    globals.myproxy_utils.delete_trustroots()