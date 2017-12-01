from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.configuration as config

@attr ('node_components')
@attr ('data')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _classic_front_ends = ['thredds', 'esg-orp']
  _docker_front_ends = ['thredds', 'esg-orp', 'esgf-auth/home']
  
  def __init__(self):
    
    if config.get(config.TEST_SECTION, config.TYPE_KEY).lower() == config.DOCKER_TEST_SET_NAME:
      front_ends = TestWebFrontEnds._docker_front_ends
    else:
      front_ends = TestWebFrontEnds._classic_front_ends
    
    AbstractWebFrontEndTestClass.__init__(self, front_ends, config.DATA_NODE_KEY)