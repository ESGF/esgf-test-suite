from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.naming as naming

@attr ('node_components')
@attr ('compute')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends = ['las']
  
  def __init__(self):
    AbstractWebFrontEndTestClass.__init__(self, TestWebFrontEnds._front_ends,
                                          naming.COMPUTE_NODE_KEY)