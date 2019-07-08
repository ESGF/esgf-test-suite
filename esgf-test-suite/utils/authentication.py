import re
import os
import subprocess
import shutil

# WORKAROUND SSL-MYPROXYCLIENT PROBLEM
# from myproxy.client import MyProxyClient, MyProxyClientGetError

import utils.configuration as config
import utils.naming as naming

from socket import error as socket_error

class MyProxyUtils(object):
  
  def __init__(self):
    
    self.cacertdir = os.path.expanduser(naming.CA_CERT_DIR_PATH)
    cert_parent_dir_path = os.path.dirname(self.cacertdir)
    if False == os.path.exists(cert_parent_dir_path):  # WORKAROUND SSL-MYPROXYCLIENT PROBLEM
      os.makedirs(cert_parent_dir_path) # WORKAROUND SSL-MYPROXYCLIENT PROBLEM
    self.credsfile = os.path.expanduser(naming.CREDENTIALS_FILE_PATH)
    self.idp_addr= config.get(config.NODES_SECTION, config.IDP_NODE_KEY).encode('ascii', 'replace')
    # self.myproxy = MyProxyClient(hostname=self.idp_addr) # WORKAROUND SSL-MYPROXYCLIENT PROBLEM
    # self.myproxy._setCACertDir(self.cacertdir) # WORKAROUND SSL-MYPROXYCLIENT PROBLEM
    self.credentials = None
    self.trustRoots = None
    self.port = '7512'
    # Reset the eventually files (for example, after a debugg session).
    self.delete_credentials()
    self.delete_trustroots()

  def get_trustroots(self):
    # Get trust roots

    #try:
    #  self.trustRoots = self.myproxy.getTrustRoots(config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY),
    #                      config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY),
    #                      writeToCACertDir=True, bootstrap=True)
    #except Exception as serr:
    #  err = "unable to connect to myproxy server '{0}' (reason: {1})"\
    #    .format(self.idp_addr, serr)
    #  assert(False), err
    
    # WORKAROUND SSL-MYPROXYCLIENT PROBLEM
    command = ['myproxy-get-trustroots', '-b', '-s', self.idp_addr, '-p', self.port]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
    process.wait()
    stdout, stderr = process.communicate()
    assert(process.returncode == 0), "fail to get the trustroots of {0} (sdtout: {1} ; stderr: {2})".format(self.idp_addr, stdout, stderr)
    self.trustRoots = {}
    for item in os.listdir(self.cacertdir):
      filename, file_extension = os.path.splitext(item)
      file_path = os.path.join(self.cacertdir, item)
      if os.path.isfile(file_path) and (file_extension == '.0' or file_extension == '.signing_policy'):
        with open(file_path, 'r') as file:
          lines = file.readlines()
          buff = ''
          for line in lines:
            buff += line
          self.trustRoots[item] = buff

  def get_credentials(self):

    #try:
      # Get credentials (and trustroots)
    #  username = config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY)
    #  password = config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY)
    #  self.credentials = self.myproxy.logon(username, password)
    #except MyProxyClientGetError as e1:
    #  err_msg = "wrong username and/or password combination when getting credentials for user '{0}' (reason: {1})"\
    #    .format(username, e1)
    #  assert(False), err_msg
    #except Exception as e2:
    #  err = "unable to connect to myproxy server '{0}' (reason: {1})"\
    #    .format(self.idp_addr, e2)
    #  assert (False), err

    # Write Credentials
    #with open(self.credsfile, 'w') as f:
    #  f.write(self.credentials[0]+self.credentials[1])
    #  os.chmod(self.credsfile, self.myproxy.PROXY_FILE_PERMISSIONS)

    # WORKAROUND SSL-MYPROXYCLIENT PROBLEM

    username = config.get(config.ACCOUNT_SECTION, config.USER_NAME_KEY)
    password = config.get(config.ACCOUNT_SECTION, config.USER_PASSWORD_KEY)
    command = ['myproxy-logon', '-S', '-T', '-s', self.idp_addr, '-p', self.port, '-l', username, '-o', self.credsfile, '-b']

    process = subprocess.run(command, input=password.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    assert(process.returncode == 0), "fail to get the credentials for {0} (sdtout: {1} ; stderr: {2})".format(self.idp_addr, process.stdout, process.stderr)

    file_content = ''
    with open(self.credsfile, 'r') as file:
      for line in file.readlines():
        file_content += line
    certs = re.findall('(-+BEGIN CERTIFICATE-+.+?-+END CERTIFICATE-+\\s+)', file_content, re.DOTALL)
    key = re.findall('(-+BEGIN RSA PRIVATE KEY-+.+?-+END RSA PRIVATE KEY-+\\s+)', file_content, re.DOTALL)
    self.credentials = (certs[0], key[0], certs[1])

  def delete_credentials(self):
    # Delete credentials file
    if os.path.exists(self.credsfile):
      os.remove(self.credsfile)

  def delete_trustroots(self):
    # Delete trustroots and cacert directory
    if os.path.exists(self.cacertdir):
      shutil.rmtree(self.cacertdir)