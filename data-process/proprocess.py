#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'syxbyi'
__version__ = '1.0.0'

from argparse import ArgumentParser
import csv
import random
from os.path import basename, dirname, join
import utils

def get_args():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest = 'subcommand')
    # Reduce dataset to smaller one
    reducer = subparser.add_parser('reduce', help = 'Reduce lines of files randomly')
    reducer.add_argument('file', help = 'File to be processed')
    reducer.add_argument('--no-header-line', help = 'Specify that the first line is not the header, so that can be reduce', action = 'store_true')
    group = reducer.add_mutually_exclusive_group()
    group.add_argument('-n', '--number', help = 'The number of lines to reduce', type = int)
    group.add_argument('-p', '--precent', help = 'For e.g. \'-p 10\' is to reduce 10 precent of data', type = int)
    # Non-numeric processing
    digitizor = subparser.add_parser('digitize', help = 'Process non-numeric items.')
    digitizor.add_argument('file', help = 'File to be processed')
    digitizor.add_argument('-M', '--mode', help = 'Choose a digitize mode: binary or remove', choices = ['binary', 'remove'])
    # if given, this column will not be process.
    digitizor.add_argument('-L', '--label', help = 'Specify the column of labels location', type = int)
    # processing single column
    column = subparser.add_parser('column', help = 'Process single column, always used to process with label column')
    column.add_argument('file', help = 'File to be processed')
    column.add_argument('--remove', help = 'Remove given column', type = int)
    column.add_argument('--move', help = 'Move a SRC column to DST', nargs = 2, type = int)
    return parser.parse_args()

class Processor(object):
    def __init__(self):
        self.args = get_args()
        self.file = basename(self.args.file)
        self.dstdir = dirname(self.args.file)
        print(self.args)
        # get label index

    def process(self):
        subcmd = self.args.subcommand
        if subcmd == 'reduce':
            self.reduce()
        elif subcmd == 'digitize':
            self.digitize()
        elif subcmd == 'column':
            self.column()
        return

    def reduce(self):
        if self.args.number is not None and self.args.number > 0:
            self.rand_reduce_n()
        elif self.args.precent is not None and self.args.precent > 0:
            self.rand_reduce_p()
        return

    def rand_reduce_n(self):
        n = self.args.number
        # get total number of lines
        with open(self.args.file, 'r') as f:
            lines = f.readlines()
        total = len(lines)
        if n >= total:
            print('!!! Total number of lines is %d, you cannot reduce %d lines' % (total, n))
            return
        print('--- Removing %d lines from a totally %d lines file' % (n, total))
        self._rand_delete(lines, total, n)
        # set target file name
        name = 'rm_%d_lines_%s' % (n, self.file)
        dst = join(self.dstdir, name)
        self._write_to_file(lines, dst)

    def rand_reduce_p(self):
        p = self.args.precent
        # get total number of lines
        with open(self.args.file, 'r') as f:
            lines = f.readlines()
        total = len(lines)
        if p >= 100:
            print('!!! Invalid precent value. You cannot remove %d precent lines from file' % p)
            return
        n = int(p / 100.0 * total)
        print('--- Removing %d precent lines: totally %d lines from file' % (p, n))
        self._rand_delete(lines, total, n)
        # set target file name
        name = '%d_precent_%s' % (100 - p, self.file)
        dst = join(self.dstdir, name)
        self._write_to_file(lines, dst)
        return

    def _rand_delete(self, lines, total, n):
        if self.args.no_header_line:
            rm_index = random.sample(range(1, total), n)
        else:
            rm_index = random.sample(range(total), n)
        for i in sorted(rm_index, reverse = True):
            del lines[i]

    def _write_to_file(self, lines, dst):
        print('--- Writing file: %s' % dst)
        with open(dst, 'w') as f:
            f.write(''.join(lines))

    # if label, this function will return 'data_line.append(label)'
    # label will be found at the last column
    def digitize(self):
        # get total column number
        with open(self.args.file, 'r') as f:
            cf = csv.reader(f)
            length = len(cf.next())
        if self.args.label is not None:
            label_index = self.args.label
            if label_index < 0:
                label_index += length
        # ask for sure
        string = 'Digitize target file: %s, with label = %s' % (self.args.file, label_index)
        if not utils.ask_for_sure(string):
            return
        non_num_index = self.get_non_numeric_index(label_index)
        mode = self.args.mode
        if mode == 'binary':
            print('!!! Not support binary processing now, sorry!')
        elif mode == 'remove':
            self.remove_non_num(non_num_index, label_index)

    # return a list containing index of non-numeric columns, and the index of label column
    def get_non_numeric_index(self, label_index = None):
        print('--- Detecting non-numeric indexes')
        with open(self.args.file, 'r') as f:
            cf = csv.reader(f)
            line = next(cf)
        def isnumeric(string):
            try:
                float(string)
                return True
            except:
                return False
        non_num_index = []
        for i,item in enumerate(line):
            if not isnumeric(item):
                non_num_index.append(i)
        print('--- Non-num indexes is: %s' % non_num_index)
        if (label_index is not None) and (label_index not in non_num_index):
            non_num_index.append(label_index)
        return non_num_index

    def remove_non_num(self, non_num_index, label_index = None):
        # set file name
        if label_index is not None:
            name = 'label_rm_num_%s' % self.file
        else:
            name = 'nolabel_rm_num_%s' % self.file
        dst = join(self.dstdir, name)
        print('--- After removed data writing to: %s' % dst)
        with open(self.args.file, 'r') as src, open(dst, 'w') as dst:
            cr = csv.reader(src)
            cw = csv.writer(dst)
            for line in cr:
                if not line:
                    continue
                tmp = []
                # remove index contained by non_num_index
                for j,item in enumerate(line):
                    if j in non_num_index:
                        continue
                    tmp.append(item)
                if label_index is not None:
                    tmp.append(line[label_index])
                cw.writerow(tmp)

    def column(self):
        return

def main():
    process = Processor()
    process.process()
    return

if __name__ == '__main__':
    main()
