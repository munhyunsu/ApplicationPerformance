#!/usr/bin/env python3

import sys
import os
import statistics
import subprocess
import re

def get_files(path, ext = '', recursive = False):
    path_list = [path]
    result = list()

    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        yield entry.path
                else:
                    if recursive == True:
                        path_list.append(entry.path)

    return path_list


def get_rtt_avg(path):
    cp = subprocess.run(['tcptrace', '-lr', path], 
            stdout = subprocess.PIPE,
            stderr = subprocess.DEVNULL,
            universal_newlines = True)
    
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('RTT avg:(?:\s)+(\d+.\d+) ms', cp.stdout)))
        if mean > 0:
            return mean
    except:
        return -1


def main(argv):
    path = argv[1]

    for path in get_files(path, '.pcap'):
        package = (path.split('/')[-1])[:-4]
        rtt = get_rtt_avg(path)
        if rtt > 0:
            print(package, rtt, sep = ', ')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
