import nose
from OpenSSL import crypto

from utils.abstract_myproxy_based_test import AbstractMyproxyBasedTest

import utils.globals as globals
from nose.plugins.attrib import attr

@attr ('node_components')
@attr ('idp')
@attr ('myproxy')
class TestMyProxy(AbstractMyproxyBasedTest):

  def __init__(self):
    AbstractMyproxyBasedTest.__init__(self)
  
  def test_get_trustroots(self):
  # Test output from get_trustroots
    assert(isinstance(globals.myproxy_utils.trustRoots, dict))
    for fileName, fileContents in globals.myproxy_utils.trustRoots.items():
      if fileName.endswith('.0'):
        # test parsing certificate 
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, fileContents)
        assert(isinstance(cert, crypto.X509))
        subj = cert.get_subject()
        assert(subj)

  def test_get_credentials(self):
    # Test output from get_trustroots
    assert(isinstance(globals.myproxy_utils.credentials, tuple))
    cert = crypto.load_certificate(crypto.FILETYPE_PEM,
                 globals.myproxy_utils.credentials[0])
    key = crypto.load_privatekey(crypto.FILETYPE_PEM,
               globals.myproxy_utils.credentials[1])
    assert(isinstance(cert, crypto.X509))
    assert(isinstance(key, crypto.PKey))