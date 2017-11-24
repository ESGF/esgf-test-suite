import nose
from nose.plugins.skip import Skip, SkipTest

from nose.plugins.attrib import attr

import utils.user as user

from utils.abstract_browser_based_test import AbstractBrowserBasedTest

import utils.globals as globals
import utils.naming as naming

@attr ('node_components')
@attr ('index')
@attr ('cog')
class TestCog(AbstractBrowserBasedTest):
  
  def __init__(self):
      
    AbstractBrowserBasedTest.__init__(self)
    self.usr = user.UserUtils()

  def test_user_login(self):

    self.usr.check_user_login(globals.browser)    

#  def test_create_user(self):

#    self.usr.check_user_exists(globals.browser)
    
#    if(self.usr.user_exists):
#      raise SkipTest("User already exists")
    
    # Create user
#    self.usr.create_user(globals.browser)
    # Test output from create_user and eventually print error message
#    assert(isinstance(self.usr.response, list)), "Didn't get any CoG response"
#    assert(self.usr.response[0] == naming.SUCCESS), "fail to create user '" + self.usr.account[naming.USER_NAME_KEY] + "'"