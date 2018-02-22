import utils.globals as globals
import utils.configuration as config
import utils.naming as naming

import urllib3

import os

from selenium.webdriver import DesiredCapabilities, Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import requests

class AbstractBrowserBasedTest(object):
  
  DEFAULT_TIMEOUT = config.get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY) # seconds
  TITLE_FOR_404 = 'Page not found'
  DOWNLOAD_DIR_PATH='/tmp'

  _firefox_profile = None
  _firefox_capabilities = None

  def __init__(self):
    if globals.browser == None:
      
      soft = config.get(config.BROWSER_SECTION, config.BROWSER_KEY)
      is_headless = config.get(config.BROWSER_SECTION,
                               config.BROWSER_IS_HEADLESS_KEY).lower() == naming.TRUE
      pf={'browser.helperApps.neverAsk.saveToDisk':'application/x-netcdf, application/netcdf',
          'browser.download.manager.closeWhenDone':True,
          'browser.download.manager.showWhenStarting':False,
          'browser.download.folderList':2,
          'browser.download.dir':AbstractBrowserBasedTest.DOWNLOAD_DIR_PATH}
      
      kwargs = dict()

      AbstractBrowserBasedTest._firefox_profile = FirefoxProfile() # profile
      AbstractBrowserBasedTest._firefox_profile.set_preference('extensions.logging.enabled', False)
      AbstractBrowserBasedTest._firefox_profile.set_preference('network.dns.disableIPv6', False)

      for key, value in pf.items():
        AbstractBrowserBasedTest._firefox_profile.set_preference(key, value)

      AbstractBrowserBasedTest._firefox_capabilities = DesiredCapabilities().FIREFOX
      AbstractBrowserBasedTest._firefox_capabilities["marionette"] = True

      if is_headless:
        os.environ.update({"MOZ_HEADLESS": '1'})
        binary = FirefoxBinary()
        binary.add_command_line_options('-headless')
        kwargs['firefox_binary'] = binary

      globals.browser = Firefox(AbstractBrowserBasedTest._firefox_profile,
                                capabilities = AbstractBrowserBasedTest._firefox_capabilities,
                                **kwargs)
      globals.browser.set_page_load_timeout(self.DEFAULT_TIMEOUT)

      urllib3.disable_warnings()
      
  def load_page(self, url, expected_element=(By.TAG_NAME, 'html'), timeout=DEFAULT_TIMEOUT):

    try:
      r = requests.get(url, verify=False, timeout=timeout)
      err_msg = "fail to connect to '{0}' (code = {1})".format(url, r.status_code)
      assert(r.status_code < 403), err_msg
    except Exception as e:
      err_msg = "fail to connect to '{0}'".format(url)
      assert(False), err_msg
    
    if(timeout != self.DEFAULT_TIMEOUT):
      globals.browser.set_page_load_timeout(timeout)
    
    try:
      globals.browser.get(url)
    except TimeoutException:
      assert(False), "timeout waiting for {0}".format(url)

    element = expected_conditions.presence_of_element_located(expected_element)
    try:
      WebDriverWait(globals.browser, timeout).until(element)
    except TimeoutException:
      assert(False), "timeout waiting for {0}".format(url)

    if(timeout != self.DEFAULT_TIMEOUT):
      globals.browser.set_page_load_timeout(self.DEFAULT_TIMEOUT)

  def wait_loading(self, msg,
                   expected_element=(By.TAG_NAME, 'html'),
                   not_expected_element=None,
                   test_expected_element=None,
                   timeout=DEFAULT_TIMEOUT):

    # Wait for the DOM to be ready
    element = expected_conditions.presence_of_element_located((By.TAG_NAME, 'html'))
    try:
      WebDriverWait(globals.browser, timeout).until(element)
    except TimeoutException:
      assert(False), "timeout waiting for {0}".format(msg)

    # The is supposed to be loaded. Let's search the not_expected_element.
    if(not_expected_element):
      try:
        by = not_expected_element[0]
        value = not_expected_element[1]
        element = globals.browser.find_element(by, value)
        if(element.text):
          assert(False), "fail to {0} (reason: '{1}')".format(msg, element.text)
        else:
          assert(False), "fail to {0}".format(msg)
      except NoSuchElementException:
        pass

    # If the not_expected_element is not found, let's wait for the good element
    # page loading may take time, so use WebDriverWait. Error page don't take time.
    if(expected_element != (By.TAG_NAME, 'html')):
      try:
        element = expected_conditions.presence_of_element_located(expected_element)
        WebDriverWait(globals.browser, timeout).until(element)
      except TimeoutException:
        assert(False), "timeout waiting for {0}".format(msg)

    if(test_expected_element):
      by = expected_element[0]
      value = expected_element[1]
      element = globals.browser.find_element(by, value)
      test_expected_element(element)

  # Call this method so as to avoid side effects between runs of test.
  def reset_browser(self):

    globals.browser.close()
    globals.browser.start_session(capabilities = AbstractBrowserBasedTest._firefox_capabilities,\
                                  browser_profile = AbstractBrowserBasedTest._firefox_profile)
    globals.browser.delete_all_cookies() # Belt and Braces.