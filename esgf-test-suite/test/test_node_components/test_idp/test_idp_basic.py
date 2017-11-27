from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.naming as naming
from testconfig import config

@attr ('node_components')
@attr ('idp')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _classic_front_ends = ['esgf-idp']
  _docker_front_ends = ['esgf-slcs/admin', 'esgf-idp']
  
  def __init__(self):
    
    if config[naming.TEST_SECTION][naming.TYPE_KEY].lower() == naming.DOCKER_TEST_SET_NAME:
      front_ends = TestWebFrontEnds._docker_front_ends
    else:
      front_ends = TestWebFrontEnds._classic_front_ends
    
    AbstractWebFrontEndTestClass.__init__(self, front_ends, naming.IDP_NODE_KEY)