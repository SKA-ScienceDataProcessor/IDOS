#!/usr/bin/python

import json
import os
import argparse
from os.path import isdir, join
from shutil import copyfile
import drivecasa
import simulate
import time
import numpy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BDA script runner.',
                                     epilog='')
    parser.add_argument('config', type=str, nargs='?', help='JSON config file.')
    args = parser.parse_args()
    if args.config is None:
        parser.print_usage()
        print "%s: error: too few arguments" % os.path.basename(__file__)
        exit(1)
    if not os.path.isfile(args.config):
        print "Error: Config file '%s' not found!" % args.config
        exit(1)

    try:
        settings = json.load(open(args.config))
    except ValueError as e:
        print 'ERROR: FAILED TO PARSE JSON CONFIG FILE!!'
        print e.message
        exit(1)

    simulate.run(settings)
    
