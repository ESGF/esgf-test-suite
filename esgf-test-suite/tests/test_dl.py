from utils.abstract_browser_based_test import AbstractBrowserBasedTest
from utils.abstract_myproxy_based_test import AbstractMyproxyBasedTest
from nose.plugins.attrib import attr

import os
import subprocess
from operator import itemgetter
from nose.plugins.skip import SkipTest
import requests

import utils.globals as globals

import utils.configuration as config
import utils.catalog as cat

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

import utils.networking as networking

import utils.naming as naming

from selenium.common.exceptions import WebDriverException

@attr ('node_components')
@attr ('data')
@attr ('dl')
class TestDataDownload(AbstractBrowserBasedTest, AbstractMyproxyBasedTest):
  
  _DOWNLOADED_FILE_PATH='/tmp/dest_file.nc'
  
  def __init__(self):
    AbstractBrowserBasedTest.__init__(self)
    AbstractMyproxyBasedTest.__init__(self)
    
    self._tu = cat.ThreddsUtils()
    print("[DEBUG] starting endpoints computation")
    self._endpoints = self._tu.get_endpoints()
    
    self.data_node = config.get(config.NODES_SECTION, config.DATA_NODE_KEY)
    self.idp_node = config.get(config.NODES_SECTION, config.IDP_NODE_KEY)
    self.username = config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY)
    self.password = config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY)
    print("[DEBUG] end of TestDataDownload initialization")

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
    print(("url downloaded: {0}".format(url)))
    try:
      r = requests.get(url, verify=False, timeout=config\
            .get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY), stream=True)
      if r.status_code == 200:
        return # as file has been downloaded and credential wasn't needed.
    except Exception as e:
      err_msg = "fail to download '{0}' (reason: {1})".format(url, e)
      assert (False), err_msg
    
    # else open a globals.browser and give the credential so as to download the file.

    self.load_page(url, (By.ID, 'SubmitButton'), timeout=config\
      .get_int(config.TEST_SECTION, config.DOWNLOAD_TIMEOUT_KEY))

    OpenID = "https://{0}/esgf-idp/openid/{1}".format(self.idp_node, self.username)

    try:
      globals.browser.find_element_by_class_name('custom-combobox-input')\
                   .send_keys(OpenID)
    except NoSuchElementException:
      assert(False), "{0} is corrupted or not compliant with esgf-test-suite".format(url)
    
    globals.browser.find_element_by_id('SubmitButton').click()

    msg = "load the openID page {0}".format(OpenID)
    self.wait_loading(msg, (By.ID, 'password'), (By.CLASS_NAME, 'errorbox'),\
      timeout=config.get_int(config.TEST_SECTION, config.DOWNLOAD_TIMEOUT_KEY))
  
    globals.browser.find_element_by_id('password').send_keys(self.password)
    
    try:
      globals.browser.find_element_by_xpath("//input[@value='SUBMIT']").click()
      msg = "authentication with username '{0}'".format(self.username)
      self.wait_loading(msg, not_expected_element=(By.ID, 'null.errors'))
      # TODO check file hash ==> create a test data set
    except WebDriverException as e:
      reason = str(e)
      if 'fileNotFound' in reason:
        reason = 'not found'
      err_msg = "fail to download '{0}' (reason: {1})".format(url, reason)
      assert (False), err_msg

  @attr ('dl_gridftp')
  def test_dl_gridftp(self):

    self.gridftp_node = config.get(config.NODES_SECTION, config.GRIDFTP_NODE_KEY)

    gridftp_port = naming.GRIDFTP_PORT_NUMBER

    is_enable = networking.ping_tcp_port(self.gridftp_node, gridftp_port)
    err_msg = "gridftp server not found at {0} port {1} (reason: {2})"\
      .format(self.gridftp_node, gridftp_port, is_enable[2])
    assert(is_enable[0]), err_msg

    path = self._get_endpoint_path('GridFTP')
    url = "gsiftp://{0}:{1}//{2}".format(self.gridftp_node, gridftp_port, path)
    print(("url downloaded: {0}".format(url)))
    
    os.environ['X509_USER_PROXY'] = globals.myproxy_utils.credsfile
    os.environ['X509_CERT_DIR'] = globals.myproxy_utils.cacertdir
    command = ['globus-url-copy', '-b', url, TestDataDownload._DOWNLOADED_FILE_PATH]

    process = subprocess.run(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             timeout=60)

    assert(process.returncode == 0), "fail to download by GridFTP (sdtout: {0} ; stderr: {1})".format(process.stdout, process.stderr)

  @classmethod
  def teardown_class(self):
    # Delete downloaded file
    if os.path.exists(TestDataDownload._DOWNLOADED_FILE_PATH):
      os.remove(TestDataDownload._DOWNLOADED_FILE_PATH)  
