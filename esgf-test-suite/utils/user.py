import requests

import utils.configuration as config
import utils.naming as naming

from selenium.webdriver.common.by import By

from abstract_browser_based_test import AbstractBrowserBasedTest
import utils.globals as globals

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class UserUtils(AbstractBrowserBasedTest):

  def __init__(self):

    self.idp_server = config.get(config.NODES_SECTION, config.IDP_NODE_KEY)
    
    # Abort test if esgf-web-fe is not reachable
    url = "https://{0}/user/add".format(self.idp_server)
    r = requests.get(url, verify=False, timeout=config.get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY))
    assert r.status_code == 200, "Fail to connect to '" + url + "'"

    # Mapping user data to fit to web-fe user creation form 
    self.elements = {'first_name'       : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_FIRST_NAME_KEY),
                     'last_name'        : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_LAST_NAME_KEY),
                     'email'            : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_EMAIL_KEY),
                     'username'         : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_NAME_KEY),
                     'password'         : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_PASSWORD_KEY),
                     'confirm_password' : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_PASSWORD_KEY),
                     'institution'      : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_INSTITUTION_KEY),
                     'city'             : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_CITY_KEY),
                     'country'          : config.get(config.ACCOUNT_SECTION,
                                                     config.USER_COUNTRY_KEY)}

  def login_user(self):

    does_user_exist = self.check_user_exists()
    
    err_msg = "User '{0}' doesn't exist for '{1}'".format(
                                config.get(config.ACCOUNT_SECTION,
                                config.USER_NAME_KEY),
                                self.idp_server)
    assert(does_user_exist), err_msg

    # Clear the browser from any previsous login.
    globals.browser.delete_all_cookies()

    URL = "https://{0}/login".format(self.idp_server)
    OpenID = "https://{0}/esgf-idp/openid/".format(self.idp_server)
    
    self.load_page(URL, (By.ID, 'openid_identifier'))

    globals.browser.find_element_by_id('openid_identifier').send_keys(OpenID)
    globals.browser.find_element_by_xpath("//input[@value='Login']").click()

    self.wait_loading('load the login page', (By.ID, 'username'), (By.CLASS_NAME, 'error-box'))

    # After check_user_exists, the page is asking for the user's password.
    globals.browser.find_element_by_id('username').send_keys(config.get(config.ACCOUNT_SECTION,
                                        config.USER_NAME_KEY))
    globals.browser.find_element_by_id('password').send_keys(config.get(config.ACCOUNT_SECTION,
                                        config.USER_PASSWORD_KEY))
    globals.browser.find_element_by_xpath("//input[@value='SUBMIT']").click()

    msg = "login with user '{0}' for '{1}'".format(config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY), self.idp_server)
    #text = 'Invalid OpenID and/or Password combination'
    self.wait_loading(msg, not_expected_element=(By.ID, 'null.errors'))
  
  def check_user_exists(self):
    
    # Clear the browser from any previsous login.
    globals.browser.delete_all_cookies()

    URL = "https://{0}/login".format(self.idp_server)
    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_server,
                       config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY))

    self.load_page(URL, (By.ID, 'openid_identifier'))

    globals.browser.find_element_by_id('openid_identifier').send_keys(OpenID)
    globals.browser.find_element_by_xpath("//input[@value='Login']").click()

    self.wait_loading('load the login confirmation')

    #text = 'OpenID Discovery Error: unrecognized by the Identity Provider'
    try:
        element_present = globals.browser.find_element_by_class_name('error-box')
        does_user_exist = False
    except NoSuchElementException:
        does_user_exist = True
    
    return does_user_exist
    
  def create_user(self):
    
    # Clear the browser from any previsous login.
    globals.browser.delete_all_cookies()

    URL = "https://{0}/user/add".format(self.idp_server)
    
    self.load_page(URL, (By.NAME, 'first_name'))

    # Filling the form
    for element_name in self.elements:
      globals.browser.find_element_by_name(element_name).send_keys(self.elements[element_name])

    globals.browser.find_element_by_xpath("//input[@value='Submit']").click()

    msg = "create user '{0}' in {1}. May be the captcha is on. "\
           "Check if USE_CAPTCHA in "\
           "/usr/local/cog/cog_config/cog_settings.cfg is set to False and "\
           "restart esg-node.".format(config.get(config.ACCOUNT_SECTION,
                                                    config.USER_NAME_KEY),
                                         config.get(config.NODES_SECTION,
                                                    config.IDP_NODE_KEY))

    self.wait_loading(msg, not_expected_element=(By.CLASS_NAME, 'errorlist'))
    # message-box and Thank you for creating an account. You can now login.