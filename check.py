#!/usr/bin/env python

import subprocess, time, yaml, os
from stathat import StatHat
from datetime import datetime

def now():
  return int(datetime.now().strftime('%s'))

def log(data):
  print '[%s] %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data)

def log_speedtest(stathat_key, stathat_prefix):
  cmdfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tespeed', 'tespeed.py')
  command = ['python', cmdfile, '-w', '-s']
  csv = subprocess.check_output(command)
  data = csv.strip().split(',')
  StatHat().ez_post_value(stathat_key, '%s_speedtest_down' % stathat_prefix, float(data[0]))
  StatHat().ez_post_value(stathat_key, '%s_speedtest_up' % stathat_prefix, float(data[1]))
  log('Data sent to StatHat')

def main():
  lastcheck = 0
  configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml')
  config = yaml.load(open(configfile, 'r').read())
  while True:
    if lastcheck < now() - 1800:
      try:
        start = now()
        log_speedtest(config['stathat_key'], config['stathat_prefix'])
        lastcheck = start
      except subprocess.CalledProcessError:
        log('Test failed, not logging.')
      except:
        log('Dafuq? This should not happen. Retrying in 10s...')
    time.sleep(10)

if __name__ == '__main__':
  main()

