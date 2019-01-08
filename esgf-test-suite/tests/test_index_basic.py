from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.configuration as config

@attr ('node_components')
@attr ('index')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends_docker    = ['projects/testproject', 'solr/#', 'esg-search/search', 'esg-orp/home.htm']
  _front_ends_installer = ['', 'solr/#', 'esg-search/search', 'esg-orp/home.htm']
  
  def __init__(self):
    
    if config.get(config.TEST_SECTION, config.TYPE_KEY).lower() == config.DOCKER_TEST_SET_NAME:
      front_ends=TestWebFrontEnds._front_ends_docker
    else:
      front_ends=TestWebFrontEnds._front_ends_installer
        
    AbstractWebFrontEndTestClass.__init__(self, front_ends, config.INDEX_NODE_KEY)