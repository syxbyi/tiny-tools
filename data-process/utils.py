#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'syxbyi'
__version__ = '1.0.0'

from argparse import ArgumentParser
import sys

class Parser(object):
    def __init__(self):
        self.parser = ArgumentParser()
        self._set_args()
        self.args = self.parser.parse_args()

    def _set_args(self):
        self.parser.add_argument('datafile', help = 'File to be processed', nargs = '?')
        self.parser.add_argument('-k', help = 'K value', type = int)

    def get_data(self):
        return self.args.datafile

    def get_k(self):
        return self.args.k

def ask_for_sure(string):
    string += ' [y/n]'
    if sys.version_info[0] < 3:
        answer = raw_input(string)
    else:
        answer = input(string)
    if answer in ['y', 'yes', 'Y']:
        return True
    return False

def main():
    return

if __name__ == '__main__':
    main()

