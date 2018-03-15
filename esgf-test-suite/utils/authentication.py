import os
import shutil

from myproxy.client import MyProxyClient, MyProxyClientGetError

import utils.configuration as config
import utils.naming as naming

from socket import error as socket_error

class MyProxyUtils(object):
  
  def __init__(self):
    
    self.cacertdir = os.path.expanduser(naming.CA_CERT_DIR_PATH)
    self.credsfile = os.path.expanduser(naming.CREDENTIALS_FILE_PATH)
    self.idp_addr= config.get(config.NODES_SECTION, config.IDP_NODE_KEY).encode('ascii', 'replace')
    self.myproxy = MyProxyClient(hostname=self.idp_addr)
    self.myproxy._setCACertDir(self.cacertdir)
    self.credentials = None
    self.trustRoots = None
    # Reset the eventually files (for example, after a debugg session).
    self.delete_credentials()
    self.delete_trustroots()

  def get_trustroots(self):
    # Get trust roots

    try:
      self.trustRoots = self.myproxy.getTrustRoots(config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY),
                          config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY),
                          writeToCACertDir=True, bootstrap=True)
    except socket_error as serr:
      err = "unable to connect to myproxy server '{0}' (reason: {1})"\
        .format(self.idp_addr, serr)
      assert(False), err

  def get_credentials(self):

    try:
      # Get credentials (and trustroots)
      username = config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY)
      password = config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY)
      self.credentials = self.myproxy.logon(username, password)
    except MyProxyClientGetError as e1:
      err_msg = "wrong username and/or password combination when getting credentials for user '{0}' (reason: {1})"\
        .format(username, e1)
      assert(False), err_msg
    except socket_error as e2:
      err = "unable to connect to myproxy server '{0}' (reason: {1})"\
        .format(self.idp_addr, e2)
      assert (False), err

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