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
        os.system('export NIX_PATH=localpkgs={}/default.nix:$NIX_PATH'.format(repo_dir))
        if os.path.exists('{}/.pmpm'.format(home)) is False:
            self._out('no pmpm directory exists, creating ...')
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/'.format(home)])
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/localrepo'.format(home)])
            proc = subprocess.run(['mkdir', '-p', '{}/.pmpm/localrepo/pkgs'.format(home)])
            proc = subprocess.run(['cp', './base.nix', '{}/default.nix'.format(repo_dir)])

    def _package_from_scratch(self):
        self._out('packaging from scratch ...')
        p_pkg = {}
        p_pkg['depends'] = input('depends on? pkg,pkg: ')
        depends = {}
        dep_csplit = p_pkg['depends'].split(',')
        for item in dep_csplit:
            item_colsplit = item.split(':')
            if len(item_colsplit) == 1:
                item_colsplit.append('latest')
            depends[item_colsplit[0]] = item_colsplit[1]
        p_pkg['depends'] = depends
        p_pkg['name'] = input('package name: ')
        p_pkg['version'] = input('package version: ')
        p_pkg['src'] = input('source path or url: ')
        if 'http' in p_pkg['src'].lower():
            p_pkg['src_sha256'] = input('source sha256: ')
        p_pkg['meta'] = {}
        p_pkg['meta']['desc'] = input('short description: ')
        p_pkg['meta']['long_desc'] = input('long description: ')
        p_pkg['meta']['homepage'] = input('project url: ')
        p_pkg['bld'] = {}
        p_pkg['bld']['steps'] = True if input('build steps? [y/n]: ').lower() == 'y' else False
        if p_pkg['bld']['steps'] is False:
            p_pkg['bld']['fp'] = input('path to build file: ')
        else:
            build_steps = []
            collect = True
            while collect:
                viable = ['a', 'e', 'd', 'c']
                out = ['you currently have {} build steps'.format(len(build_steps))]
                out.insert(0, 'source: {}'.format(p_pkg['src']))
                for step in build_steps:
                    out.append('{0}: {1}'.format(build_steps.index(step), step))
                out.append('(a)dd, (e)dit, (d)elete, (c)ontinue: ')
                selection = input('\n'.join(out))
                if selection in viable:
                    if selection == 'a':
                        build_steps.append(input('enter shell command: '))
                    elif selection == 'e':
                        try:
                            bs_index = int(input('enter line number to edit: '))
                        except ValueError as ve:
                            input('invalid value: {} press enter to continue'.format(bs_index))
                            continue
                        self._out('current: \n{}'.format(build_steps[bs_index]))
                        build_steps[bs_index] = input('new value: ')
                    elif selection == 'd':
                        try:
                            bs_index = int(input('enter line number to delete: '))
                        except ValueError as ve:
                            input('invalid value: {} press enter to continue'.format(bs_index))
                            continue
                        build_steps.pop(bs_index)
                    else:
                        for step in build_steps:
                            self._out('{0}: {1}'.format(build_steps.index(step), step))
                        collect = True if input('confirm? [y/n]: ').lower() == 'n' else False
                p_pkg['bld']['script'] = build_steps
        return p_pkg

    def _package(self):
        pkg_dir = self._args.OPTS
        pkg_json_fp = '{}package.json'.format(pkg_dir)
        pkg_json = {}
        if self._args.prompt:
            pkg_json = self._package_from_scratch()
        else:
            if os.path.exists(pkg_dir):
                if os.path.exists(pkg_json_fp):
                    try:
                        pkg_json = json.load(open(pkg_json_fp))
                    except json.decoder.JSONDecodeError as jde:
                        self._out('bad json: {0}\n{1}'.format(pkg_json_fp, jde))
                    self._out('got package.json for {}'.format(pkg_dir))
                else:
                    self._out('no package.json found for {}'.format(pkg_dir))
            else:
                self._out('package directory does not exist')
        self._process_package(pkg_json)

    def _process_package(self, pkg_json):
        pkg_template = [x.strip() for x in open('package.nix', 'r').readlines()]
        src = pkg_json['src']
        pkg_template[4] = '  version = "{}";'.format(pkg_json['version'])
        pkg_template[5] = '  name = "{}'.format(pkg_json['name'])
        pkg_template[5] += '-${version}";'
        if not 'http' in src:
            pkg_template[0] = '{ stdenv }:'
            del(pkg_template[7:11])
            pkg_template.insert(7, '  src = {};'.format(src))
        else:
            pkg_template[8] = '  url = "{}";'.format(pkg_json['src'])
            pkg_template[9] = '  sha256 = "{}";'.format(pkg_json['src_sha256'])
        builder_index = 0
        for line in pkg_template:
            if 'builder =' in line:
                builder_index = pkg_template.index(line) + 2
        if pkg_json['bld'].get('script'):
            for step in pkg_json['bld']['script']:
                pkg_template.insert(builder_index, '    {}'.format(step))
                builder_index += 1
        else:
            del(pkg_template[builder_index-2:builder_index+2])
            pkg_template.insert(builder_index-2, '  builder = {}'.format(pkg_json['bld']['fp']))
        line = pkg_template[0]
        end = line.index(':')
        new_line = line[:end-2]
        for dep in pkg_json['depends']:
           new_line += ', {}'.format(dep)
        new_line += ' }: '            
        pkg_template[0] = new_line
        meta_index = 0
        for line in pkg_template:
            if 'meta = {' in line:
                meta_index = pkg_template.index(line)
        pkg_template[meta_index+1] = '    description = "{}";'.format(pkg_json['meta']['desc'])
        pkg_template[meta_index+2] = '    longDescription = "{}";'.format(pkg_json['meta']['long_desc'])
        pkg_template[meta_index+3] = '    homepage = "{}";'.format(pkg_json['meta']['homepage'])
        self._write_package(pkg_template, pkg_json)

    def _write_package(self, pkg_template, pkg_json):
        home = os.path.expanduser('~')
        repo_dir = '{}/.pmpm/localrepo'.format(home)
        pkg_name = pkg_json['name']
        dest_dir = '{0}/pkgs/{1}'.format(repo_dir, pkg_name)
        self._out('creating new package {} in localrepo ...'.format(pkg_name))
        proc = subprocess.run(['mkdir', '-p', '{}'.format(dest_dir)])
        with open('{}/default.nix'.format(dest_dir), 'w') as pkg_fp:
            pkg_fp.write('\n'.join(pkg_template))
        self._out('done writing package content ...')
        self._out('updating localrepo registry to include new package ...')
        base_nix_fp = '{}/default.nix'.format(repo_dir)
        base_nix = [x.strip() for x in open(base_nix_fp, 'r').readlines()]
        self_index = 0
        abort_write = False
        for line in base_nix:
            if 'self = {' in line:
                self_index = base_nix.index(line)
            if pkg_json['name'] in line and 'callPackage' in line:
                abort_write = True
        pkg_insert = '    {0} = callPackage ./pkgs/{1} {{ }};'.format(pkg_json['name'], pkg_json['name'])
        base_nix.insert(self_index+1, pkg_insert)
        if not abort_write:
            with open(base_nix_fp, 'w') as bn_fp:
                bn_fp.write('\n'.join(base_nix))
        proc = subprocess.run(['nix-env', '-f', "<localpkgs>", '-iA', pkg_json['name']])
 
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

    def _install(self):
        target = self._args.OPTS
        if target is None:
            self._out('no install target specified')
            return
        proc = subprocess.run(['nix-env', '-f', "<localpkgs>", '-f', "<nixpkgs>", '--install', target])

    def _uninstall(self):
        target = self._args.OPTS
        if target is None:
            self._out('no uninstall target specified')
            return
        proc = subprocess.run(['nix-env', '-f', "<localpkgs>", '-f', "<nixpkgs>", '--uninstall', target])

    def _search(self):
        search_str = self._args.OPTS
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
        cmd = ['nix-env', '-qaP', '-f', "<localpkgs>", '--description', '{}'.format(search_str)]
        proc = subprocess.run(cmd)

    def _process_args(self):
        self._arg_parser = argparse.ArgumentParser()
        self._arg_parser.add_argument('COMMAND', nargs='?')
        self._arg_parser.add_argument('OPTS', nargs='?')
        self._arg_parser.add_argument('-d', '--dry', help='run dry', action='store_true')
        self._arg_parser.add_argument('-p', '--prompt', help='prompt mode', action='store_true')
        self._arg_parser.add_argument('-l', '--local', help='run local', action='store_true')
        self._arg_parser.add_argument(
                '--version',
                help='print version',
                action='store_true')
        self._args = self._arg_parser.parse_args()

if __name__ == '__main__':
    app = Pmpm()
