
import utils.naming as naming
import utils.configuration as config

is_debug = config.get(config.SYSTEM_SECTION, config.IS_DEBUG_KEY).lower() == naming.TRUE

browser = None

myproxy_utils = None