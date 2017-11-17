import os
import shutil

from myproxy.client import MyProxyClient
from OpenSSL import crypto

from testconfig import config
import utils.naming as naming

class MyProxyUtils(object):
  
  def __init__(self):
    self.cacertdir = os.path.expanduser("~/.esg/certificates")
    self.credsfile = os.path.expanduser("~/.esg/credentials.pem")
    idp_addr= config[naming.NODES_SECTION][naming.IDP_NODE_KEY].encode('ascii', 'replace')
    self.myproxy = MyProxyClient(hostname=idp_addr)
    self.myproxy._setCACertDir(self.cacertdir)


  def get_trustroots(self):
    # Get trust roots
    self.trustRoots = self.myproxy.getTrustRoots(config[naming.ACCOUNT_SECTION][naming.USER_NAME_KEY],
                        config[naming.ACCOUNT_SECTION][naming.USER_PASSWORD_KEY],
                        writeToCACertDir=True, bootstrap=True)

  def get_credentials(self):
    # Get credentials (and trustroots)
    self.credentials = self.myproxy.logon(config[naming.ACCOUNT_SECTION][naming.USER_NAME_KEY],
                         config[naming.ACCOUNT_SECTION][naming.USER_PASSWORD_KEY])
    # Write Credentials
    with open(self.credsfile, 'w') as f:
      f.write(self.credentials[0]+self.credentials[1])
      os.chmod(self.credsfile, self.myproxy.PROXY_FILE_PERMISSIONS)
  

  def delete_credentials(self):
    # Delete credentials file
    if os.path.exists(self.credsfile):
      os.remove(self.credsfile)


  def delete_trustroots(self):
    # Delete trustroots and cacert directory
    if os.path.exists(self.cacertdir):
      shutil.rmtree(self.cacertdir)