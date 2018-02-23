import utils.globals as globals

import os

from utils.abstract_browser_based_test import AbstractBrowserBasedTest

def setup_package():
  if(globals.is_debug):
    print("*********** begin setup package")

def teardown_package():
  if(globals.is_debug):
    print("*********** begin teardown package")

  if globals.browser != None and not globals.is_debug:
    globals.browser.quit()
  
  if globals.myproxy_utils != None and not globals.is_debug:
    globals.myproxy_utils.delete_credentials()
    globals.myproxy_utils.delete_trustroots()

  if(not globals.is_debug\
     and os.path.exists(AbstractBrowserBasedTest.GECKODRIVER_LOG_FILE_PATH)):
    os.remove(AbstractBrowserBasedTest.GECKODRIVER_LOG_FILE_PATH)  