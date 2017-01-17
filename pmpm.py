#!/usr/bin/env python
import argparse
import os
import subprocess

class Pmpm(object):
    def __init__(self):
        self._VERSION = '0.0.1'
        self._process_args()
        self._execute()

    def _execute(self):
        if self._args.version:
            print('pmpm v{}'.format(self._VERSION))
            return
        cmd = self._args.COMMAND
        if cmd == 'install':
            self._install()
        elif cmd == 'uninstall':
            self._uninstall()
        elif cmd == 'package':
            elf._package()
        elif cmd == 'search':
            self._search()
        else:
            self._arg_parser.print_help()

    def _search(self):
        search_string = self._args.OPTS
        print('\n-\nlocally installed\n-\n')
        local_cmd = ['nix-env', '-qP', '--description', '{}'.format(search_string)]
        proc = subprocess.run(local_cmd)
        if self._args.local:
            return
        print('\n-\nglobal results\n-\n')
        global_cmd = ['nix-env', '-qaP', '--description', '{}'.format(search_string)]
        proc = subprocess.run(global_cmd)

    def _process_args(self):
        self._arg_parser = argparse.ArgumentParser()
        self._arg_parser.add_argument('COMMAND', nargs='?')
        self._arg_parser.add_argument('OPTS', nargs='?')
        self._arg_parser.add_argument('-d', '--dry', help='dry run', action='store_true')
        self._arg_parser.add_argument('-l', '--local', help='apply locally', action='store_true')
        self._arg_parser.add_argument(
                '--version',
                help='print version',
                action='store_true')
        self._args = self._arg_parser.parse_args()

if __name__ == '__main__':
    app = Pmpm()
