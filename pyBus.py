#!/usr/bin/python

import os
import sys
import time
import signal
import traceback
import logging
import argparse
import gzip
import pyBus_core as core

#####################################
# FUNCTIONS
#####################################
# Manage Ctrl+C gracefully
def signal_handler_quit(signal, frame):
  logging.info("Shutting down pyBus")
  core.shutdown()
  sys.exit(0)

# Print basic usage
def print_usage():
  print "Intended Use:"
  print "%s <PATH_TO_DEVICE>" % (sys.argv[0])
  print "Eg: %s /dev/ttyUSB0" % (sys.argv[0])
  
#################################
# Configure Logging for pySel
#################################
def configureLogging(numeric_level):
  if not isinstance(numeric_level, int):
    numeric_level=0
  logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s [%(levelname)s in %(module)s] %(message)s', 
    datefmt='%Y/%m/%dT%I:%M:%S'
  )
  
def createParser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='count', default=0, help='Increases verbosity of logging.')
  parser.add_argument('--device', action='store', help='Path to iBus USB interface (Bought from reslers.de)')
  return parser

#####################################
# MAIN
#####################################
def __main__():
  parser   = createParser()
  results  = parser.parse_args()
  loglevel = results.verbose
  _startup_cwd = os.getcwd()
  
  signal.signal(signal.SIGINT, signal_handler_quit) # Manage Ctrl+C
  configureLogging(loglevel)
  
  devPath = sys.argv[1] if (len(sys.argv) > 1) else "/dev/ttyUSB0"
  core.DEVPATH = devPath if devPath else "/dev/ttyUSB0"
  
  try:
    core.initialize()
    core.run()
  except Exception:
    logging.error("Caught unexpected exception:")
    logging.error(traceback.format_exc())
  
  logging.critical("And I'm dead.")    
  sys.exit(0)

if __name__ == '__main__':
  __main__()
