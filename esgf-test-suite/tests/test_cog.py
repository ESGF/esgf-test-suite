import nose
from nose.plugins.skip import Skip, SkipTest

from nose.plugins.attrib import attr

import utils.user as user

from utils.abstract_browser_based_test import AbstractBrowserBasedTest

import utils.globals as globals
import utils.naming as naming

import utils.configuration as config

import sys

from selenium.webdriver.common.by import By

@attr ('node_components')
@attr ('index')
@attr ('cog')
class TestCog(AbstractBrowserBasedTest):
  
  def __init__(self):
      
    AbstractBrowserBasedTest.__init__(self)
    sys.tracebacklimit = 0
    self.usr = user.UserUtils()
  
  @attr ('cog_user_login')
  def test_cog_user_login(self):

    self.usr.login_user()    
    
  @attr ('cog_root_login')
  def test_cog_root_login(self):
    
    # Alway start with this method so as to dodge side effects.
    self.reset_browser()
    
    index_node=config.get(config.NODES_SECTION, config.INDEX_NODE_KEY)
    url = "https://{0}/login2".format(index_node)
    
    self.load_page(url)

    globals.browser.find_element_by_id('id_username')\
                   .send_keys(config.get(config.COG_SECTION, config.ADMIN_USERNAME_KEY))

    globals.browser.find_element_by_id('id_password')\
                   .send_keys(config.get(config.COG_SECTION, config.ADMIN_PASSWORD_KEY))

    globals.browser.find_element_by_xpath("//input[@value='Login']").click()
      
    msg = "log onto the Cog admin page of '{0}'"\
          .format(index_node)
    
    self.wait_loading(msg, not_expected_element=(By.CLASS_NAME, 'errornote'))
    
  @attr ('cog_create_user')
  def test_cog_create_user(self):

    does_user_exist=self.usr.check_user_exists()

    if(does_user_exist):
      assert(False), "user '{0}' already exists".format(config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY))
    else:
      self.usr.create_user() # Create user
