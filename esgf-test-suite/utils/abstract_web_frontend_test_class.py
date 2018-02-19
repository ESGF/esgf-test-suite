import requests

from configuration_exception import ConfigurationException

import utils.configuration as config
from nose.plugins.attrib import attr

class AbstractWebFrontEndTestClass(object):
  
  def __init__(self, front_ends, node_key_name):
    
    node_name = config.get(config.NODES_SECTION, node_key_name)
    requests.packages.urllib3.disable_warnings()
    self._front_ends = front_ends
    self._node_name = node_name
  
  def check_url(self, url):
    r = requests.get(url, verify=False, timeout=config.get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY))
    assert r.status_code == 200, "Fail to connect to '" + url + "'"
    
  @attr ('basic_ping')
  def test_frontends_availability(self):
    for front_end in self._front_ends:
      url = "https://" + self._node_name + "/" + front_end
      yield self.check_url, url