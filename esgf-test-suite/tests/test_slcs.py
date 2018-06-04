from nose.plugins.attrib import attr

import utils.configuration as config
from utils.abstract_browser_based_test import AbstractBrowserBasedTest

import utils.globals as globals

from selenium.webdriver.common.by import By

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
  def test_slcs_django_admin_login(self):
    
    # Alway start with this method so as to dodge side effects.
    self.reset_browser()

    url = "https://{0}/esgf-slcs/admin".format(self.idp_node)
    
    self.load_page(url, (By.ID, 'id_username'))

    globals.browser.find_element_by_id('id_username').send_keys(self.username)
    globals.browser.find_element_by_id('id_password').send_keys(self.password)
    globals.browser.find_element_by_xpath("//input[@value='Log in']").click()

    msg = "log onto the SLCS django admin page of {0}"\
          .format(url)
    
    self.wait_loading(msg, (By.CLASS_NAME, 'dashboard'), (By.CLASS_NAME, 'errornote'))