#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'syxbyi'
__version__ = '1.0.0'

from configparser import ConfigParser
from argparse import ArgumentParser
import sys
import subprocess

class Sshtool(object):
    def __init__(self):
        self.cfgparser = ConfigParser()
        self.cfgparser.read('config.ini')
        self.argparser = ArgumentParser()
        self._init_args()
        self.args = self.argparser.parse_args()
        self.run = self.args.run

    def _init_args(self):
        self.argparser.add_argument('target', help = 'Specify target host and hostname', nargs = '?')
        group = self.argparser.add_mutually_exclusive_group()
        group.add_argument('-r', '--run', help = 'Directly run ssh command in program, rather than print it', action = 'store_true')
        group.add_argument('-p', '--print', dest = 'p', help = 'Just print command to stdout, donot run', action = 'store_true')
        self.argparser.add_argument('--scp', help = 'Copy file, rather than ssh. (Format: --scp src dst)', nargs = 2)

    def _get_target(self):
        sections = self.cfgparser.sections()
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

    def _get_cmd(self):
        ip = self.cfgparser.get(self.target, 'ip')
        hostname = self.cfgparser.get(self.target, 'hostname')
        if self.args.scp:
            scp = self.args.scp
            self.cmd = 'scp %s %s@%s:%s' % (scp[0], hostname, ip, scp[1])
        else:
            self.cmd = 'ssh %s@%s' % (hostname, ip)

    def _ask_for_run(self):
        if not self.args.run:
            string = 'Run command directly? [y/n]'
            if sys.version_info[0] < 3:
                answer = raw_input(string)
            else:
                answer = input(string)
            if answer in ['y', 'yes', 'Y']:
                return True
        return False

    def ssh(self):
        self._get_target()
        self._get_cmd()
        if self.args.p:
            print(self.cmd)
            return
        if self.args.run or self._ask_for_run():
            subprocess.call(self.cmd, shell = True)

def main():
    sshtool = Sshtool()
    sshtool.ssh()
    return

if __name__ == '__main__':
    main()

