import nose
from OpenSSL import crypto

from utils.abstract_myproxy_based_test import AbstractMyproxyBasedTest

import utils.globals as globals
from nose.plugins.attrib import attr

import utils.configuration as config

from nose.plugins.skip import Skip, SkipTest

@attr ('node_components')
@attr ('idp')
@attr ('myproxy')
class TestMyProxy(AbstractMyproxyBasedTest):

  def __init__(self):
    AbstractMyproxyBasedTest.__init__(self)
  
  @attr ('myproxy_get_trustroots')
  def test_myproxy_get_trustroots(self):

    # Test output from get_trustroots
    if(globals.myproxy_utils.trustRoots):
      err_msg = "unsupported trusted root certificate format '{0}'".format(globals.myproxy_utils.trustRoots)
      assert(isinstance(globals.myproxy_utils.trustRoots, dict)), err_msg
      for fileName, fileContents in list(globals.myproxy_utils.trustRoots.items()):
        if fileName.endswith('.0'):
          # test parsing certificate
          cert = crypto.load_certificate(crypto.FILETYPE_PEM, fileContents)
          assert(isinstance(cert, crypto.X509)), "unsupported certificate format '{0}'".format(cert)
          subj = cert.get_subject()
          err_msg = "fail to get the trusted root certificates for '{0}'".format(config.get(config.NODES_SECTION, config.IDP_NODE_KEY))
          assert(subj), err_msg
    else:
      raise SkipTest("unable to check the trustroots")

  @attr ('myproxy_get_credentials')
  def test_myproxy_get_credentials(self):

    # Test output from get_credentials
    if(globals.myproxy_utils.credentials):
      err_msg = "unsupported credentials format '{0}'".format(globals.myproxy_utils.credentials)
      assert(isinstance(globals.myproxy_utils.credentials, tuple)), err_msg
      cert = crypto.load_certificate(crypto.FILETYPE_PEM,
                   globals.myproxy_utils.credentials[0])
      key = crypto.load_privatekey(crypto.FILETYPE_PEM,
                 globals.myproxy_utils.credentials[1])
      assert(isinstance(cert, crypto.X509)), "unsupported certificate format '{0}'".format(cert)
      assert(isinstance(key, crypto.PKey)), "unsupported cryptographic key format '{0}'".format(key)
    else:
      raise SkipTest("unable to check the credentials")