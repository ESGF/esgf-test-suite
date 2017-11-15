from utils.abstract_basic_test_class import AbstractBasicTestClass
from nose.plugins.attrib import attr

from utils.configuration_exception import ConfigurationException

import utils.naming as naming

from testconfig import config

@attr ('node_components')
@attr ('index')
@attr ('basic')
class TestWebFrontEnds(AbstractBasicTestClass):
  
  _front_ends = ['projects/testproject', 'solr/#', 'esg-search/search', 'esg-orp', 'esgf-auth/home', 'esgf-slcs/admin']
  
  def __init__(self):
    err_msg = 'the value of the key ' + naming.INDEX_NODE_KEY_NAME + ' in section ' + naming.NODES_SECTION_NAME + ', is not found'
    
    try:
      node_name = config[naming.NODES_SECTION_NAME][naming.INDEX_NODE_KEY_NAME]
    except KeyError:
      raise ConfigurationException(err_msg)
      
    if node_name.isspace():
      raise ConfigurationException(err_msg)
    else:
      AbstractBasicTestClass.__init__(self, TestWebFrontEnds._front_ends, node_name)