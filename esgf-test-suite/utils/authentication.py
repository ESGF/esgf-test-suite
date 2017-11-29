import os
import shutil

from myproxy.client import MyProxyClient
from OpenSSL import crypto

import utils.configuration as config
import utils.naming as naming

class MyProxyUtils(object):
  
  def __init__(self):
    
    self.cacertdir = os.path.expanduser(naming.CA_CERT_DIR_PATH)
    self.credsfile = os.path.expanduser(naming.CREDENTIALS_FILE_PATH)
    idp_addr= config.get(config.NODES_SECTION, config.IDP_NODE_KEY).encode('ascii', 'replace')
    self.myproxy = MyProxyClient(hostname=idp_addr)
    self.myproxy._setCACertDir(self.cacertdir)


  def get_trustroots(self):
    # Get trust roots
    self.trustRoots = self.myproxy.getTrustRoots(config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY),
                        config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY),
                        writeToCACertDir=True, bootstrap=True)

  def get_credentials(self):
    # Get credentials (and trustroots)
    self.credentials = self.myproxy.logon(config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY),
                         config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY))
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