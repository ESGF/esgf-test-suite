from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.naming as naming

@attr ('node_components')
@attr ('data')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends = ['thredds', 'esg-orp']
  
  def __init__(self):
    AbstractWebFrontEndTestClass.__init__(self, TestWebFrontEnds._front_ends,
                                          naming.DATA_NODE_KEY)