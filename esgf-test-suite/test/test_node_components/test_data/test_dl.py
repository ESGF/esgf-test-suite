from utils.abstract_browser_based_test import AbstractBrowserBasedTest
from utils.abstract_myproxy_based_test import AbstractMyproxyBasedTest
from nose.plugins.attrib import attr

import os
import subprocess
from operator import itemgetter
from nose.plugins.skip import Skip, SkipTest
import requests

import utils.globals as globals

import utils.configuration as config
import utils.catalog as cat

from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass

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
      raise SkipTest("no available endpoints at {1}".format(service, self.data_node))
    else:
      service_endpoints = [i for i in self._endpoints if service in i[2]] #Sort by service
      if not service_endpoints:
        raise SkipTest("no available {0} endpoints at {1}".format(service, self.data_node))
      else:
        path = min(service_endpoints,key=itemgetter(1))[0] #Pick smallest dataset 
        return path
  
  @attr ('dl_http')
  def test_dl_http(self):

    # Alway start with this method so as to dodge side effects.
    self.reset_browser()

    path = self._get_endpoint_path('HTTPServer')
    url = "http://{0}/thredds/fileServer/{1}".format(self.data_node, path)

    try:
      r = requests.get(url, verify=False, timeout=config\
            .get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY), stream=True)
      if r.status_code == 200:
        return # as file has been downloaded and credential wasn't needed.
    except Exception as e:
      err_msg = "fail to download '{0}'".format(url)
      assert (False), err_msg
    
    # else open a globals.browser and give the credential so as to download the file.

    self.load_page(url, (By.ID, 'SubmitButton'), timeout=config\
      .get_int(config.TEST_SECTION, config.DOWNLOAD_TIMEOUT_KEY))

    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_node, self.username)

    globals.browser.find_element_by_class_name('custom-combobox-input')\
                   .send_keys(OpenID)
    
    globals.browser.find_element_by_id('SubmitButton').click()

    msg = "load the openID page {0}".format(OpenID)
    self.wait_loading(msg, (By.ID, 'password'), (By.CLASS_NAME, 'errorbox'),\
      timeout=config.get_int(config.TEST_SECTION, config.DOWNLOAD_TIMEOUT_KEY))
  
    globals.browser.find_element_by_id('password').send_keys(self.password)
    globals.browser.find_element_by_xpath("//input[@value='SUBMIT']").click()

    msg = "authentication with username '{0}'".format(self.username)
    self.wait_loading(msg, not_expected_element=(By.ID, 'null.errors'))

    # TODO check file hash ==> create a test data set

  @attr ('dl_gridftp')
  def test_dl_gridftp(self):

    path = self._get_endpoint_path('GridFTP')
    url = "gsiftp://{0}:2811//{1}".format(self.data_node, path)
    os.environ['X509_USER_PROXY'] = globals.myproxy_utils.credsfile
    os.environ['X509_CERT_DIR'] = globals.myproxy_utils.cacertdir
    command = ['globus-url-copy', '-b', url, TestDataDownload._DOWNLOADED_FILE_PATH]
    process = subprocess.Popen(command)
    process.wait()
    assert(process.returncode == 0), "fail to download by GridFTP"

  @classmethod
  def teardown_class(self):
    # Delete downloaded file
    if os.path.exists(TestDataDownload._DOWNLOADED_FILE_PATH):
      os.remove(TestDataDownload._DOWNLOADED_FILE_PATH)  