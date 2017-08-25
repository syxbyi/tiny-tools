#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'syxbyi'
__version__ = '1.0.0'

from configparser import ConfigParser
from argparse import ArgumentParser
import sys
import subprocess

class Parser(object):
    def __init__(self):
        self.cfgparser = ConfigParser()
        self.cfgparser.read('config.ini')
        self.argparser = ArgumentParser()
        self._init_args()
        self.args = self.argparser.parse_args()

    def _init_args(self):
        self.argparser.add_argument('target', help = 'Specify target host and hostname', nargs = '?')
        self.argparser.add_argument('-r', '--run', help = 'Directly run ssh command in program, rather than print it', action = 'store_true')

    def get_target(self):
        sections = [s.encode('ascii') for s in self.cfgparser.sections()]
        target = self.args.target
        if not target or target not in sections:
            print(sections)
            string = 'Please choose from the list with the target host you want to ssh to: '
            if sys.version_info[0] < 3:
                section = raw_input(string)
            else:
                section = input(string)
            if section in sections:
                target = section
            else:
                exit('Sorry, cannot find your target host')
        self.target = target

    def get_cmd(self):
        ip = self.cfgparser.get(self.target, 'ip')
        hostname = self.cfgparser.get(self.target, 'hostname')
        self.cmd = 'ssh %s@%s' % (hostname, ip)

    def run(self):
        self.get_target()
        self.get_cmd()
        if self.args.run:
            subprocess.call(self.cmd, shell = True)
        else:
            print(self.cmd)

def main():
    parser = Parser()
    parser.run()
    return

if __name__ == '__main__':
    main()

