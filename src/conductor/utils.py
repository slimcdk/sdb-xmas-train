import os, signal
from datetime import datetime, time

def get_env(key, fallback):
    value = os.environ.get(key)
    if (value is None):
        return fallback
    return value


def parse_time_from_string (time_str):
    try:
        h = int(time_str[0:2])
        m = int(time_str[3:5])
        s = int(time_str[6:8])
        return time(h,m,s)
    except Exception:
        pass
    exit(1)



class GracefulKiller:
  # https://stackoverflow.com/a/31464349/2591014

  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True
