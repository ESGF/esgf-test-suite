from test_index_node.test_basic import TestWebFrontEnds
from utils.abstract_test_class import AbstractTestClass

import nose

from nose.config import Config

from nose.plugins.attrib import AttributeSelector

class Toto(object):

    def __init__(self):
        self.eval_attr = ''
        self.attr = ''

config = {"index_node":"vesgdev-idx.ipsl.upmc.fr"}
AbstractTestClass._config= config

# run per test file
#nose.main(defaultTest='test_index_node/test_basic.py')

nose_conf = Config()
nose_conf.verbosity = 3

# run test files only located in the given path
#nose_conf.configureWhere('test_index_node')
#nose.main(config=nose_conf)

# run test with the following attributes
options = Toto()
options.attr = 'basic'
attr_selector = AttributeSelector()
attr_selector.configure(options, nose_conf)
nose.main(config=nose_conf, plugins=(attr_selector))

#import subprocess
#result = subprocess.call(['nosetests', '-a toto -vv --exe --nocapture --nologcapture --collect-only'])
