from utils.abstract_basic_test_class import AbstractBasicTestClass
from nose.plugins.attrib import attr

from utils.configuration_exception import ConfigurationException

import utils.naming as naming

@attr ('node_components')
@attr ('index')
@attr ('basic')
class TestWebFrontEnds(AbstractBasicTestClass):
  
  _front_ends = ['solr/#'] #['projects/testproject', 'solr/#', 'esg-search/search', 'esg-orp', 'esgf-auth/home', 'esgf-slcs/admin']
  
  def __init__(self):
    
    node_name = self._config[naming.INDEX_NODE_KEY]
    if (not node_name) or node_name.isspace():
      raise ConfigurationException('value for the key index_node is not found')
    else:
      AbstractBasicTestClass.__init__(self, TestWebFrontEnds._front_ends, node_name)