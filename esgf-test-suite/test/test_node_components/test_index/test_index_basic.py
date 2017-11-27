from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.naming as naming
from testconfig import config

@attr ('node_components')
@attr ('index')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends_docker    = ['projects/testproject', 'solr/#', 'esg-search/search', 'esg-orp']
  _front_ends_installer = ['', 'solr/#', 'esg-search/search', 'esg-orp']
  
  def __init__(self):
    
    if config[naming.TEST_SECTION][naming.TYPE_KEY].lower() == naming.DOCKER_TEST_SET_NAME:
      front_ends=TestWebFrontEnds._front_ends_docker
    else:
      front_ends=TestWebFrontEnds._front_ends_installer
        
    AbstractWebFrontEndTestClass.__init__(self, front_ends, naming.INDEX_NODE_KEY)