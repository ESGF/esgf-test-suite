from splinter import Browser

import utils.globals as globals

from testconfig import config
import utils.naming as naming

class AbstractBrowserBasedTest(object):
  
  def __init__(self):
    if globals.browser == None:
      soft = config[naming.BROWSER_SECTION][naming.BROWSER_KEY]
      is_headless = config[naming.BROWSER_SECTION][naming.BROWSER_IS_HEADLESS_KEY].lower() == naming.TRUE
      globals.browser = Browser(soft, headless=is_headless)