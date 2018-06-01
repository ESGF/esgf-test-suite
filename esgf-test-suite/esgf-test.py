import nose
from utils.reporting import Reporting

if __name__ == '__main__':
  nose.main(addplugins=[Reporting()])