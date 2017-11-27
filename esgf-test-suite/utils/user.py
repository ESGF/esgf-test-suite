import requests
from splinter import Browser

import utils.configuration as config
import utils.naming as naming

from abstract_browser_based_test import AbstractBrowserBasedTest

class UserUtils(object):

  def __init__(self):

    self.idp_server = config.get(config.NODES_SECTION, config.IDP_NODE_KEY)
    
    # Abort test if esgf-web-fe is not reachable
    url = "https://{0}/user/add".format(self.idp_server)
    r = requests.get(url, verify=False, timeout=1)
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

  def login_user(self, browser):

    does_user_exist = self.check_user_exists(browser)
    err_msg = "User '{0}' doesn't exist for '{1}'".format(
                                config.get(config.ACCOUNT_SECTION,
                                config.USER_NAME_KEY),
                                self.idp_server)
    assert(does_user_exist), err_msg
    
    URL = "https://{0}/login".format(self.idp_server)
    OpenID = "https://{0}/esgf-idp/openid/".format(self.idp_server)

    # Try to log in
    browser.visit(URL)
    browser.find_by_id('openid_identifier').fill(OpenID)
    browser.find_by_value('Login').click()
       
    # After check_user_exists, the page is asking for the user's password.
    browser.find_by_id('username').fill(config.get(config.ACCOUNT_SECTION,
                                        config.USER_NAME_KEY))
    browser.find_by_id('password').fill(config.get(config.ACCOUNT_SECTION,
                                        config.USER_PASSWORD_KEY))
    browser.find_by_value('SUBMIT').click()
    
    def func():
      return browser.is_text_not_present('Invalid OpenID and/or Password combination')
    
    test_result = AbstractBrowserBasedTest.find_or_wait_until(func, "user login")
    err_msg = "Fail to login with user '{0}' for '{1}'".format(
      config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY), self.idp_server)    
    assert(test_result), err_msg
  
  def check_user_exists(self, browser):
    URL = "https://{0}/login".format(self.idp_server)
    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_server,
                       config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY))

    # Try to log in
    browser.visit(URL)
    browser.find_by_id('openid_identifier').fill(OpenID)
    browser.find_by_value('Login').click()
    
    # User does not exist if unable to resolve OpenID
    def func():
      return browser.is_text_not_present('OpenID Discovery Error: unrecognized by the Identity Provider')
    
    does_user_exist = AbstractBrowserBasedTest.find_or_wait_until(func,
                                                           "check user account")
    return does_user_exist
    
  def create_user(self, browser):
    URL = "https://{0}/user/add".format(self.idp_server)
    browser.visit(URL)
  
    # Filling the form
    for element_name in self.elements:
      browser.find_by_name(element_name).fill(self.elements[element_name])

    browser.find_by_value('Submit').click()
    
    def func():
      return browser.is_text_present("Thank you for creating an account. You can now login.")
    
    is_account_created = AbstractBrowserBasedTest.find_or_wait_until(func,
                                                             "creating account")
        
    # Parsing response
    self.response = []    
    if (is_account_created):
      self.response.append(naming.SUCCESS)
    else:
      self.response.append(naming.FAILURE)