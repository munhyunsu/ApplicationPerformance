import os
import sys


def main():
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pcap',
                         type=str,
                         required=True,
                         help='root directory of pcap')
    parser.add_argument('-x', '--xml',
                         type=str,
                         required=True,
                         help='root directory of xml')
    parser.add_argument('-i', '--info',
                         type=str,
                         required=True,
                         help='result file about SI,FP,LL,CS,RT')
    parser.add_argument('-o', '--output',
                         type=str,
                         required=True,
                         help='output file location')
    ARGS = parser.parse_args()

    main()

