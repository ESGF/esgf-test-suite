from nose.plugins.attrib import attr

import utils.configuration as config
from utils.abstract_browser_based_test import AbstractBrowserBasedTest

import utils.globals as globals

@attr ('node_components')
@attr ('idp')
@attr ('slcs')
class TestSlcs(AbstractBrowserBasedTest):
  
  def __init__(self):
    AbstractBrowserBasedTest.__init__(self)
    self.idp_node = config.get(config.NODES_SECTION, config.IDP_NODE_KEY)
    self.username = config.get(config.SLCS_SECTION, config.ADMIN_USERNAME_KEY)
    self.password = config.get(config.SLCS_SECTION, config.ADMIN_PASSWORD_KEY)

  @attr ('slcs_django_admin_login')  
  def test_0_login_django_admin_interface(self):
    url = "https://{0}/esgf-slcs/admin".format(self.idp_node)
    globals.browser.visit(url)
    globals.browser.find_by_id('id_username').fill(self.username)
    globals.browser.find_by_id('id_password').fill(self.password)
    globals.browser.find_by_value('Log in').click()
    
    def func():
      result = globals.browser.is_text_not_present("correct username and password")
      result &= globals.browser.is_text_not_present("Please correct the error below")
      return result
   
    is_passed = self.find_or_wait_until(func, "admin login")
    err_msg = "Fail to connect to admin page of '{0}' with '{1}'".\
      format(self.idp_node, self.username)
    assert(is_passed), err_msg