from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.naming as naming

@attr ('node_components')
@attr ('idp')
@attr ('basic')
@attr ('docker')
class TestDockerWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends = ['esgf-slcs/admin', 'esgf-idp']
  
  def __init__(self):
    AbstractWebFrontEndTestClass.__init__(self, TestWebFrontEnds._front_ends,
                                          naming.IDP_NODE_KEY)
@attr ('node_components')
@attr ('idp')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends = ['esgf-idp']
  
  def __init__(self):
    AbstractWebFrontEndTestClass.__init__(self, TestWebFrontEnds._front_ends,
                                          naming.IDP_NODE_KEY)