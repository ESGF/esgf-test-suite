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
class TestCreateUser(AbstractBrowserBasedTest):
  
  def test_create_user(self):
    
    AbstractBrowserBasedTest.__init__(self)

    usr = user.UserUtils()
    usr.check_user_exists(globals.browser)
    
    if(usr.user_exists):
      raise SkipTest("User already exists")
    
    # Create user
    usr.create_user(globals.browser)
    # Test output from create_user and eventually print error message
    assert(isinstance(usr.response, list))
    assert(usr.response[0] == naming.SUCCESS), usr.response