from testconfig import config
from configuration_exception import ConfigurationException

import sys

############################ CONFIGURATION KEYS ################################

### SECTION 'NODES'

NODES_SECTION    = 'nodes'

INDEX_NODE_KEY   = 'index_node'
IDP_NODE_KEY     = 'idp_node'
DATA_NODE_KEY    = 'data_node'
COMPUTE_NODE_KEY = 'compute_node'

### SECTION 'ACCOUNT'

ACCOUNT_SECTION       = 'account'

USER_FIRST_NAME_KEY  = 'firstname'
USER_LAST_NAME_KEY   = 'lastname'
USER_EMAIL_KEY       = 'email'
USER_NAME_KEY        = 'username'
USER_PASSWORD_KEY    = 'password'
USER_INSTITUTION_KEY = 'institution'
USER_CITY_KEY        = 'city'
USER_COUNTRY_KEY     = 'country'

### SECTION 'BROWSER'

BROWSER_SECTION         = 'browser'

BROWSER_KEY             = 'soft'
BROWSER_IS_HEADLESS_KEY = 'is_headless'

### SECTION 'COG'

COG_SECTION        = 'cog'

ADMIN_USERNAME_KEY = 'admin_username'
ADMIN_PASSWORD_KEY = 'admin_password'

### SECTION 'SLCS'

SLCS_SECTION        = 'slcs'

ADMIN_USERNAME_KEY = 'admin_username'
ADMIN_PASSWORD_KEY = 'admin_password'

### SECTION 'TEST'

TEST_SECTION = 'test'

TYPE_KEY     = 'type'
WEB_PAGE_TIMEOUT_KEY  = 'web_page_timeout'
DOWNLOAD_TIMEOUT_KEY  = 'download_timeout'

### SECTION 'SYSTEM'

SYSTEM_SECTION = 'sys'

IS_DEBUG_KEY   = 'is_debug'  

################################## SPECIAL VALUES ##############################

DOCKER_TEST_SET_NAME = 'docker'

CLASSIC_TEST_SET_NAME = 'classic'

################################### FUNCTIONS ##################################

_buffer=dict()

def _get_section(section_name):
  
  try:
    section = config[section_name]
  except Exception:
    err_msg = "[CONF] missing configuration section '{0}'".format(section_name)
    raise ConfigurationException(err_msg)

  return section

def get(section_name, key_name):
  
  if _buffer.has_key(section_name):
    if _buffer[section_name].has_key(key_name):
      return _buffer[section_name][key_name]
    else:
      section = _get_section(section_name) # fetch the value of the key.
      # Don't create a section in the buffer, it already exists.
  else:
    section = _get_section(section_name)
    _buffer[section_name] = dict()
  
  result = _assert_config_key(section, section_name, key_name)
  _buffer[section_name][key_name] = result
  
  return result

def get_int(section_name, key_name):
  try:
    string_value = get(section_name, key_name)
    return int(string_value)
  except ValueError:
    err_msg = "[CONF] convertion error in the section '{0}', entry '{1}': can't read '{2}' as an integer"\
      .format(section_name, key_name, string_value)
    print >> sys.stderr, err_msg
    exit(-1)

def get_float(section_name, key_name):
  try:
    string_value = get(section_name, key_name)
    return float(string_value)
  except ValueError:
    err_msg = "[CONF] convertion error in the section '{0}', entry '{1}': can't read '{2}' as a float"\
      .format(section_name, key_name, string_value)
    print >> sys.stderr, err_msg
    exit(-1)

def _assert_config_key(section, section_name, key_name):
  
  try:
    value = section[key_name]
  except Exception:
    err_msg = "[CONF] missing key '{0}' in section '{1}'".format(key_name, section_name)
    raise ConfigurationException(err_msg)  

  err_msg = "[CONF] missing value for key '{0}' in section '{1}'".format(key_name, section_name)
  
  if not value or value.isspace():
    raise ConfigurationException(err_msg)
 
  return value