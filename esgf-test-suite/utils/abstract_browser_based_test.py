from splinter import Browser

import utils.globals as globals
import utils.configuration as config
import utils.naming as naming

import urllib3

from selenium.common.exceptions import StaleElementReferenceException
import time

class AbstractBrowserBasedTest(object):
  
  DEFAULT_TIMEOUT = 3 # seconds
  
  def __init__(self):
    if globals.browser == None:
      
      soft = config.get(config.BROWSER_SECTION, config.BROWSER_KEY)
      is_headless = config.get(config.BROWSER_SECTION,
                               config.BROWSER_IS_HEADLESS_KEY).lower() == naming.TRUE
      pf={'browser.helperApps.neverAsk.saveToDisk':'application/x-netcdf, application/netcdf',
          'browser.download.manager.closeWhenDone':True,
          'browser.download.manager.showWhenStarting':False}
      globals.browser = Browser(soft, headless=is_headless, profile_preferences=pf)
      urllib3.disable_warnings()
      
  @staticmethod
  def find_or_wait_until(function_to_execute, err_msg, timeout=DEFAULT_TIMEOUT):
    starting_time = time.time()
    ending_time = starting_time + timeout
    while(time.time() < ending_time):
      try:
        return function_to_execute()
      except StaleElementReferenceException:
        time.sleep(0.1)
    raise Exception('Timeout waiting for {0}'.format(err_msg))