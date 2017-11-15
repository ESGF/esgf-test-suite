import requests
from abstract_test_class import AbstractTestClass

class AbstractBasicTestClass(AbstractTestClass):
  
  def __init__(self, front_ends, node_name):
    requests.packages.urllib3.disable_warnings()
    self._front_ends = front_ends
    self._node_name = node_name
  
  def check_url(self, url):
    r = requests.get(url, verify=False, timeout=5)
    assert r.status_code == 200

  def test_frontends_availability(self):
    for front_end in self._front_ends:
      url = "https://" + self._node_name + "/" + front_end
      print(url)
      yield self.check_url, url