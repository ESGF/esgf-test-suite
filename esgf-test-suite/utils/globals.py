
from testconfig import config

import utils.naming as naming

is_debug = config[naming.SYSTEM_SECTION][naming.IS_DEBUG_KEY].lower() == naming.TRUE

browser = None

myproxy_utils = None