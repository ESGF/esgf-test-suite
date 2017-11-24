import nose
from nose.plugins.skip import Skip, SkipTest

from nose.plugins.attrib import attr

import utils.user as user

from utils.abstract_browser_based_test import AbstractBrowserBasedTest

import utils.globals as globals
import utils.naming as naming

from testconfig import config

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
    
    url = "https://{0}/login2".format(config[naming.NODES_SECTION][naming.IDP_NODE_KEY])
    globals.browser.visit(url)
    globals.browser.find_by_id('id_username').fill(config[naming.COG_SECTION][naming.ADMIN_USERNAME_KEY])
    globals.browser.find_by_id('id_password').fill(config[naming.COG_SECTION][naming.ADMIN_PASSWORD_KEY])
    globals.browser.find_by_value('Login').click()
    
    err_msg = "Fail to connect to admin page of '{0}'".format(config[naming.NODES_SECTION][naming.IDP_NODE_KEY])
    assert(not globals.browser.is_text_present("Your username and password didn't match. Please try again")), err_msg

#  def test_create_user(self):

#    self.usr.check_user_exists(globals.browser)
    
#    if(self.usr.user_exists):
#      raise SkipTest("User already exists")
    
    # Create user
#    self.usr.create_user(globals.browser)
    # Test output from create_user and eventually print error message
#    assert(isinstance(self.usr.response, list)), "Didn't get any CoG response"
#    assert(self.usr.response[0] == naming.SUCCESS), "fail to create user '" + self.usr.account[naming.USER_NAME_KEY] + "'"