#!/usr/bin/env python
import argparse
import json
import os
import subprocess

class Pmpm(object):
    def __init__(self):
        self._VERSION = '0.0.1'
        self._process_args()
        self._verify_local_repo()
        self._execute()

    def _out(self, msg):
        print('[pmpm]: {}'.format(msg))

    def _verify_local_repo(self):
        home = os.path.expanduser('~')
        repo_dir = '{}/.pmpm/localrepo'.format(home)
        if os.path.exists('{}/.pmpm'.format(home)) is False:
            self._out('no pmpm directory exists, creating ...')
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/'.format(home)])
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/localrepo'.format(home)])
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/pkgs'.format(home)])
            proc = subprocess.run(['cp', './base.nix', '{}/default.nix'.format(repo_dir)])
        
    def _package(self):
        '''
            package points to a directory with a json file
            that json file hooks it all up
            
            TODO
            if "src" in JSON has http or HTTPS, thats a fetchurl that needs
            to customize the json.
            1) "depends" needs fetchurl added
            2) fetchurl {} section is added w/ source url and sha256

        '''
        pkg_dir = self._args.OPTS
        pkg_json_fp = '{}package.json'.format(pkg_dir)
        if os.path.exists(pkg_dir):
            if os.path.exists(pkg_json_fp):
                try:
                    pkg_json = json.load(open(pkg_json_fp))
                except json.decoder.JSONDecodeError as jde:
                    self._out('bad json: {0}\n{1}'.format(pkg_json_fp, jde))
                self._out('got package.json for {}'.format(pkg_dir))
                self._process_package(pkg_json)
            else:
                self._out('no package.json found for {}'.format(pkg_dir))
        else:
            self._out('package directory does not exist')

    def _process_package(self, pkg_json):
        self._out(pkg_json)

    def _execute(self):
        if self._args.version:
            self._out('pmpm v{}'.format(self._VERSION))
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
        self._out('---')
        self._out('locally installed')
        self._out('---')
        local_cmd = ['nix-env', '-qP', '--description', '{}'.format(search_string)]
        proc = subprocess.run(local_cmd)
        if self._args.local:
            return
        self._out('---')
        self._out('available')
        self._out('---')
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
