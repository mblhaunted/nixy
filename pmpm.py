#!/usr/bin/env python
import argparse
import sys

class Pmpm(object):
    def __init__(self):
        self._VERSION = '0.0.1'
        self._process_args()

    def _process_args(self):
        self._arg_parser = argparse.ArgumentParser()
        self._arg_parser.add_argument('COMMAND')
        self._arg_parser.add_argument('OPTS', nargs='?')
        self._arg_parser.add_argument('-d', '--dry', help='dry run', action='store_true')
        self._arg_parser.add_argument('-l', '--list', help='list', action='store_true')
        self._arg_parser.parse_args()



if __name__ == '__main__':
    app = Pmpm()
