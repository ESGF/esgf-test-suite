from utils.abstract_browser_based_test import AbstractBrowserBasedTest
from utils.abstract_myproxy_based_test import AbstractMyproxyBasedTest
from nose.plugins.attrib import attr

import os
import shutil
import subprocess
from operator import itemgetter
from nose.plugins.skip import Skip, SkipTest
import requests

import utils.globals as globals

import utils.authentication as auth
import utils.configuration as config
import utils.catalog as cat
import utils.user as usr

from selenium.webdriver.common.by import By

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

  def _get_endpoint_path(self, service):
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
    
    globals.browser.delete_all_cookies()

    path = self._get_endpoint_path('HTTPServer')
    url = "http://{0}/thredds/fileServer/{1}".format(self.data_node, path)

    r = requests.get(url, verify=False, timeout=10, stream=True)
    if r.status_code == 200:
      return # as file has been downloaded and credential wasn't needed.
    
    # else open a globals.browser and give the credential so as to download the file.

    self.load_page(url, (By.ID, 'SubmitButton'), timeout=15)

    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_node, self.username)

    globals.browser.find_element_by_class_name('custom-combobox-input')\
                   .send_keys(OpenID)
    
    globals.browser.find_element_by_id('SubmitButton').click()

    msg = "load the openID page {0}".format(OpenID)
    self.wait_loading(msg, (By.ID, 'password'), (By.CLASS_NAME, 'errorbox'), timeout=15)
  
    globals.browser.find_element_by_id('password').send_keys(self.password)
    globals.browser.find_element_by_xpath("//input[@value='SUBMIT']").click()

    msg = "authentication with username '{0}'".format(self.username)
    self.wait_loading(msg, not_expected_element=(By.ID, 'null.errors'))

    # TODO check file hash ==> create a test data set

  @attr ('dl_gridftp')
  def test_1_globus_url_copy(self):
    path = self._get_endpoint_path('GridFTP')
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