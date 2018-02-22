import socket

import errno

import time

import utils.configuration as config


def ping_tcp_port(host, port, timeout=config.get_int(config.TEST_SECTION, config.WEB_PAGE_TIMEOUT_KEY)):
  s = socket.socket()
  s.settimeout(timeout)
  result = False
  end = None
  err_msg = None
  try:
    start = time.time()
    s.connect((host, port))
    s.close()
    result = True
    end = time.time()
  except Exception as e:
    # Connection refused is not a failure.
    if e[0] == errno.ECONNREFUSED:
      result = True
    else:
      result = False
      err_msg = str(e)

  end = time.time()
  ms = 1000 * (end - start)

  return(result, round(ms, 2), err_msg)