
import utils.naming as naming
import utils.configuration as config

is_debug = config.get(config.SYSTEM_SECTION, config.IS_DEBUG_KEY).lower() == naming.TRUE


# At the begining of a run, nosetest instanciates the class of the tests. But, it instanciates
# as many time the same class as this class has tests. Abstract classes, in utils
# package, manage this problem. These global variables are centralized so as to
# optimize the test suite.

# Create only one instance of the browser so as to optimized the wall clock time.
# As the tests share the same browser instance, AbstractBrowserBasedTest class
# offers a convenient way to create a new session of the browser instance
# (see reset_browser).
browser = None

# Create only one instance of the myproxy utils so as to optimized the wall clock time.
myproxy_utils = None