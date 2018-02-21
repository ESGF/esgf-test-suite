import os

from nose.plugins import Plugin

class Reporting(Plugin):

  name = 'reporting'

  def options(self, parser, env=os.environ):

    super(Reporting, self).options(parser, env=env)
    self.enabled = True

  def configure(self, options, conf):

    super(Reporting, self).configure(options, conf)
    self.enabled = True

  def testName(self, test):

    result = test.address()[2].split('.')[1].split('test_')[1]

    if(result == 'basic_ping'):
      result = "{0} ({1})".format(result, test.id().split('\'')[1])

    return(result)

  def formatFailure(self, test, err):

    ec, ev, tb = err
    return('Reason', ev, '')