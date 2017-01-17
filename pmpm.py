#!/usr/bin/env python
import argparse
import os
import subprocess

class Pmpm(object):
    def __init__(self):
        self._VERSION = '0.0.1'
        self._process_args()
        self._verify_local_repo()
        self._execute()

    def _verify_local_repo(self):
        home = os.path.expanduser('~')
        repo_dir = '{}/.pmpm/localrepo'.format(home)
        if os.path.exists('{}/.pmpm'.format(home)) is False:
            print('no pmpm directory exists, creating ...')
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/'.format(home)])
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/localrepo'.format(home)])
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/pkgs'.format(home)])
            proc = subprocess.run(['cp', './base.nix', '{}/default.nix'.format(repo_dir)])
        
    def _package(self):
        '''
            package points to a directory with a json file
            that json file hooks it all up
        '''
        package_dir = self._args.OPTS
        if os.path.exists(package_dir) is True:
            print('good')
        else:
            print('package directory does not exist')

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
            self._package()
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
        self._arg_parser.add_argument('-d', '--dry', help='run dry', action='store_true')
        self._arg_parser.add_argument('-l', '--local', help='run local', action='store_true')
        self._arg_parser.add_argument(
                '--version',
                help='print version',
                action='store_true')
        self._args = self._arg_parser.parse_args()

if __name__ == '__main__':
    app = Pmpm()
