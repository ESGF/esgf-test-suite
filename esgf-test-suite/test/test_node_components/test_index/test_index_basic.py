from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.naming as naming

@attr ('node_components')
@attr ('index')
@attr ('basic')
class TestWebFrontEnds(AbstractWebFrontEndTestClass):
  
  _front_ends = ['projects/testproject', 'solr/#', 'esg-search/search', 'esg-orp', 'esgf-auth/home', 'esgf-slcs/admin']
  
  def __init__(self):
    AbstractWebFrontEndTestClass.__init__(self, TestWebFrontEnds._front_ends,
                                          naming.INDEX_NODE_KEY)