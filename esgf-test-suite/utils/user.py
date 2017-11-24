import requests
from splinter import Browser

from testconfig import config
import utils.naming as naming

class UserUtils(object):

  def __init__(self):

    self.account = config[naming.ACCOUNT_SECTION]
    self.idp_server = config[naming.NODES_SECTION][naming.IDP_NODE_KEY]
    
    # Abort test if esgf-web-fe is not reachable
    url = "https://{0}/user/add".format(self.idp_server)
    r = requests.get(url, verify=False, timeout=1)
    assert r.status_code == 200, "Fail to connect to '" + url + "'"

    # Mapping user data to fit to web-fe user creation form 
    self.elements = {'first_name'       : self.account[naming.USER_FIRST_NAME_KEY],
                     'last_name'        : self.account[naming.USER_LAST_NAME_KEY],
                     'email'            : self.account[naming.USER_EMAIL_KEY],
                     'username'         : self.account[naming.USER_NAME_KEY],
                     'password'         : self.account[naming.USER_PASSWORD_KEY],
                     'confirm_password' : self.account[naming.USER_PASSWORD_KEY],
                     'institution'      : self.account[naming.USER_INSTITUTION_KEY],
                     'city'             : self.account[naming.USER_CITY_KEY],
                     'country'          : self.account[naming.USER_COUNTRY_KEY]}

  def check_user_login(self, browser):
    self.check_user_exists(browser)
    err_msg = "User '{0}' doesn't exit for '{1}'".format(self.account[naming.USER_NAME_KEY], self.idp_server)
    assert(self.user_exists), err_msg
    
    browser.find_by_id('username').fill(self.account[naming.USER_NAME_KEY])
    browser.find_by_id('password').fill(self.account[naming.USER_PASSWORD_KEY])
    browser.find_by_value('SUBMIT').click()
    err_msg = "Fail to login with user '{0}' for '{1}'".format(self.account[naming.USER_NAME_KEY], self.idp_server)
    assert(not browser.is_text_present('Invalid OpenID and/or Password combination')), err_msg
  
  def check_user_exists(self, browser):
    URL = "https://{0}/login".format(self.idp_server)
    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_server, self.account['username'])

    # Try to log in
    browser.visit(URL)
    browser.find_by_id('openid_identifier').fill(OpenID)
    browser.find_by_value('Login').click()

    # User does not exist if unable to resolve OpenID
    if(browser.is_text_present("OpenID Discovery Error: unrecognized by the Identity Provider.")):
      self.user_exists = False
    else:
      self.user_exists = True
    
  def create_user(self, browser):
    URL = "https://{0}/user/add".format(self.idp_server)
    browser.visit(URL)
  
    # Filling the form
    for element_name in self.elements:
      browser.find_by_name(element_name).fill(self.elements[element_name])

    browser.find_by_value('Submit').click()

    # Parsing response
    self.response = []    
    if (browser.is_text_present("Thank you for creating an account. You can now login.") == True):
      self.response.append(naming.SUCCESS)
    else:
      self.response.append(naming.FAILURE)