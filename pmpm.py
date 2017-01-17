#!/usr/bin/env python
import sys

class Pmpm(object):
    def __init__(self):
        self._VERSION = '0.0.1'
        self._process_args()

    def _process_args(self):
        '''
            COMMAND [options]
            pmpm install --help
            pmpm uninstall mypackage
            pmpm package add ~/new_package/
            pmpm package remove ~/new_package/
        
        '''
        self._available_commands = ['install', 'uninstall', 'package', 'list']
        self._user_args = sys.argv[1:]
        self._parse_args()

    def _parse_args(self):
        if len(self._user_args) < 3:
            self._show_help()

    def _show_help(self, command=None):
        out = []
        if not command:
            out = ['PMPM v{}\nusage: pmpm [COMMAND] [OPTIONS]'.format(self._VERSION)]
            out.append('\navailable commands:')
            for cmd in self._available_commands:
                out.append(cmd)
            out.append('\nfor command specific help use: pmpm [COMMAND] help')
        print('\n'.join(out))


if __name__ == '__main__':
    app = Pmpm()
