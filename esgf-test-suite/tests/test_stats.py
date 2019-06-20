from utils.abstract_web_frontend_test_class import AbstractWebFrontEndTestClass
from nose.plugins.attrib import attr

import utils.configuration as config

@attr ('node_components')
@attr ('data')
@attr ('statistics')
class TestStatsFrontEnds(AbstractWebFrontEndTestClass):
  
  _stats_api = ['esgf-stats-api/cmip5/stats-by-space/xml',
                'esgf-stats-api/cmip5/stats-by-dataset/xml',
                'esgf-stats-api/cmip5/stats-by-experiment/xml',
                'esgf-stats-api/cmip5/stats-by-model/xml',
                'esgf-stats-api/cmip5/stats-by-variable/xml',
                'esgf-stats-api/obs4mips/stats-by-space/xml',
                'esgf-stats-api/obs4mips/stats-by-dataset/xml',
                'esgf-stats-api/obs4mips/stats-by-realm/xml',
                'esgf-stats-api/obs4mips/stats-by-source/xml',
                'esgf-stats-api/obs4mips/stats-by-variable/xml',
                'esgf-stats-api/cross-project/stats-by-time/xml']
  
  def __init__(self):
    AbstractWebFrontEndTestClass.__init__(self, TestStatsFrontEnds._stats_api,
                                          config.DATA_NODE_KEY)