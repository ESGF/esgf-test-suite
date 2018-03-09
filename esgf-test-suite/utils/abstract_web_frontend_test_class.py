import requests

import utils.configuration as config
from nose.plugins.attrib import attr

class AbstractWebFrontEndTestClass(object):
  
  def __init__(self, front_ends, node_key_name):
    
    node_name = config.get(config.NODES_SECTION, node_key_name)
    requests.packages.urllib3.disable_warnings()
    self._front_ends = front_ends
    self._node_name = node_name

  @staticmethod
  def check_url(url):

    try:
      r = requests.get(url, verify=False, timeout=config.get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY))
      assert r.status_code == 200, "fail to connect to '" + url + "'"
    except Exception as e:
      err_msg = "fail to connect to '{0}' (reason: {1})".format(url, e)
      assert(False), err_msg
    
  @attr ('basic_ping')
  def test_basic_ping(self):
    for front_end in self._front_ends:
      url = "https://" + self._node_name + "/" + front_end
      yield self.check_url, url