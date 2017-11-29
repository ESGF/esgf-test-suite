from utils.abstract_browser_based_test import AbstractBrowserBasedTest
from utils.abstract_myproxy_based_test import AbstractMyproxyBasedTest
from nose.plugins.attrib import attr

import os
import shutil
import subprocess
from splinter import Browser
from operator import itemgetter
from nose.plugins.skip import Skip, SkipTest
import requests

import utils.globals as globals

import utils.authentication as auth
import utils.configuration as config
import utils.catalog as cat
import utils.user as usr

@attr ('node_components')
@attr ('data')
@attr ('dl')
class TestDataDownload(AbstractBrowserBasedTest, AbstractMyproxyBasedTest):
  
  _DOWNLOADED_FILE_PATH='/tmp/dest_file.nc'
  
  def __init__(self):
    AbstractBrowserBasedTest.__init__(self)
    AbstractMyproxyBasedTest.__init__(self)
    
    self._tu = cat.ThreddsUtils()
    self._endpoints = self._tu.get_endpoints()
    self.data_node = config.get(config.NODES_SECTION, config.DATA_NODE_KEY)
    self.idp_node = config.get(config.NODES_SECTION, config.IDP_NODE_KEY)
    self.username = config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY)
    self.password = config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY)

  def get_endpoint_path(self, service):
    if not self._endpoints:
      raise SkipTest("No available endpoints at {1}".format(service, self.data_node))
    else:
      service_endpoints = [i for i in self._endpoints if service in i[2]] #Sort by service
      if not service_endpoints:
        raise SkipTest("No available {0} endpoints at {1}".format(service, self.data_node))
      else:
        path = min(service_endpoints,key=itemgetter(1))[0] #Pick smallest dataset 
        return path
  
  @attr ('dl_http')
  def test_0_http_browser_download(self):
    path = self.get_endpoint_path('HTTPServer')
    url = "http://{0}/thredds/fileServer/{1}".format(self.data_node, path)
    
    r = requests.get(url, verify=False, timeout=10, stream=True)
    
    # TODO check file hash ==> create a test data set

    if r.status_code == 200:
      return # as file has been downloaded and credential wasn't needed.
    
    # else open a globals.browser and give the credential so as to download the file.
    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_node, self.username)
    globals.browser.visit(url)

    globals.browser.find_by_css('input.custom-combobox-input').fill(OpenID)
    globals.browser.find_by_value('GO').click()

    globals.browser.find_by_id('password').fill(self.password)
    globals.browser.find_by_value('SUBMIT').click()
    
    def func():
      return globals.browser.is_text_present('Group Registration Request')
    
    is_passed = self.find_or_wait_until(func, "group registration request")
    # To do only if user is not enrolled in a group
    if is_passed:
      # Chosing First Registration Group
      globals.browser.find_by_id('button_1').click()
    
      # Accepting License Agreement
      globals.browser.execute_script('myForm.submit();')

      # Clicking on 'Download data button'
      globals.browser.find_by_id('goButton').click()
  
  @attr ('dl_globus')
  def test_1_globus_url_copy(self):
    path = self.get_endpoint_path('GridFTP')
    url = "gsiftp://{0}:2811//{1}".format(self.data_node, path)
    os.environ['X509_USER_PROXY'] = globals.myproxy_utils.credsfile
    os.environ['X509_CERT_DIR'] = globals.myproxy_utils.cacertdir
    command = ['globus-url-copy', '-b', url, TestDataDownload._DOWNLOADED_FILE_PATH]
    process = subprocess.Popen(command)
    process.wait()
    assert(process.returncode == 0), "Fail to download by GridFTP"

  @classmethod
  def teardown_class(self):
    # Delete downloaded file
    if os.path.exists(TestDataDownload._DOWNLOADED_FILE_PATH):
      os.remove(TestDataDownload._DOWNLOADED_FILE_PATH)  