import requests

from testconfig import config
from configuration_exception import ConfigurationException
import utils.naming as naming

class AbstractWebFrontEndTestClass(object):
  
  def __init__(self, front_ends, node_key_name):
    err_msg = 'the value of the key ' + node_key_name + ' in section ' + naming.NODES_SECTION_NAME + ', is not found'
    
    try:
      node_name = config[naming.NODES_SECTION_NAME][node_key_name]
    except KeyError:
      raise ConfigurationException(err_msg)

    if node_name.isspace():
      raise ConfigurationException(err_msg)

    requests.packages.urllib3.disable_warnings()
    self._front_ends = front_ends
    self._node_name = node_name
  
  def check_url(self, url):
    r = requests.get(url, verify=False, timeout=5)
    assert r.status_code == 200

  def test_frontends_availability(self):
    for front_end in self._front_ends:
      url = "https://" + self._node_name + "/" + front_end
      yield self.check_url, url