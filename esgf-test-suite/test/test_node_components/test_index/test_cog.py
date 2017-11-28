import nose
from nose.plugins.skip import Skip, SkipTest

from nose.plugins.attrib import attr

import utils.user as user

from utils.abstract_browser_based_test import AbstractBrowserBasedTest

import utils.globals as globals
import utils.naming as naming

import utils.configuration as config

@attr ('node_components')
@attr ('index')
@attr ('cog')
class TestCog(AbstractBrowserBasedTest):
  
  def __init__(self):
      
    AbstractBrowserBasedTest.__init__(self)
    self.usr = user.UserUtils()

  def test_user_login(self):

    self.usr.login_user(globals.browser)    

  def test_root_login(self):
    
    idp_node=config.get(config.NODES_SECTION, config.IDP_NODE_KEY)
    url = "https://{0}/login2".format(idp_node)
    globals.browser.visit(url)
    globals.browser.find_by_id('id_username').fill(config.get(config.COG_SECTION, config.ADMIN_USERNAME_KEY))
    globals.browser.find_by_id('id_password').fill(config.get(config.COG_SECTION, config.ADMIN_PASSWORD_KEY))
    globals.browser.find_by_value('Login').click()
    
    def func():
      return globals.browser.is_text_not_present("Your username and password didn't match. Please try again")
   
    is_passed = self.find_or_wait_until(func, "root login")
    err_msg = "Fail to connect to admin page of '{0}'".format(config.get(config.NODES_SECTION, config.IDP_NODE_KEY))
    assert(is_passed), err_msg

  def test_create_user(self):

    does_user_exist=self.usr.check_user_exists(globals.browser)
    
    if(does_user_exist):
      raise SkipTest("User already exists")
    
    # Create user
    self.usr.create_user(globals.browser)
    # Test output from create_user and eventually print error message
    assert(isinstance(self.usr.response, list)), "Didn't get any CoG response"
    assert(self.usr.response[0] == naming.SUCCESS), "Fail to create user '" + config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY) + "'"