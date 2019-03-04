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


def get_subprocess_stdout(path):
    cp = subprocess.run(['tcptrace', '--output_dir=./tmp', '-lrZ', path], 
            stdout = subprocess.PIPE,
            stderr = subprocess.DEVNULL,
            universal_newlines = True)



    return cp.stdout



def get_rttavg_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('RTT avg:(?:\s)+(\d+.\d+) ms', string)))
        return mean
    except:
        return -1

def get_rttmax_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('RTT max:(?:\s)+(\d+.\d+) ms', string)))
        return mean
    except:
        return -1



def get_idletime_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('idletime max:(?:\s)+(\d+.\d+) ms', 
                    string)))
        return mean
    except:
        return -1

   

def get_dataxmittime_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('data xmit time:(?:\s)+(\d+.\d+) secs', 
                    string)))
        return mean
    except:
        return -1



def get_tcp_len(string):
    try:
        length= len(re.findall('TCP connection', 
                    string))
        return length
    except:
        return -1



def get_http_len(string):
    try:
        length= len(re.findall(':80', 
                    string))
        return length
    except:
        return -1



def get_https_len(string):
    try:
        length = len(re.findall(':443', 
                    string))
        return length
    except:
        return -1



def get_retrans_sum(string):
    try:
        sumation = sum(map(int,
                       re.findall('rexmt data pkts:(?:\s)+(\d+)', 
                       string)))
        return sumation
    except:
        return -1


def get_trafficvolume_sum(string):
    try:
        sumation = sum(map(int,
                       re.findall('unique bytes sent:(?:\s)+(\d+)', 
                       string)))
        return sumation
    except:
        return -1



def get_ttfb_avg(string):
    try:
        result = list()
        for path in get_files('./tmp', '.dat'):
            cp = subprocess.run(['cat', path],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.DEVNULL,
                                universal_newlines = True)
            for line in cp.stdout.splitlines():
                ttfb = int(line.split(' ')[1])
                if ttfb == 0:
                    continue
                result.append(ttfb)
        mean = statistics.mean(result)
        return mean
    except:
        return 0


def get_keep_rate(string):
    try:
        target_list = re.findall('complete conn: \w*', string)
        keep_cnt = 0
        for conn in target_list:
            if conn == 'complete conn: no':
                keep_cnt = keep_cnt + 1
        return keep_cnt/len(target_list)
    except:
        return -1




### Need to change dict and dict to csv
def main(argv):
    path = argv[1]

    subprocess.run('rm ./tmp/*', shell = True)
    print('package', 'rtt', 'rttm', 'idletime', 'xmittime', 'connections', 
          'http', 'https', 'retrans', 'trafficvolume', 'ttfb', 
          'keep', sep = ',')
    for path in get_files(path, '.pcap'):
        string = get_subprocess_stdout(path)

        package = (path.split('/')[-1])[:-5]
        rtt = get_rttavg_avg(string)
        rttm = get_rttmax_avg(string)
        idletime = get_idletime_avg(string)
        xmittime = get_dataxmittime_avg(string)
        tcp = get_tcp_len(string)
        http = get_http_len(string)
        https = get_https_len(string)
        retrans = get_retrans_sum(string)
        trafficvolume = get_trafficvolume_sum(string)
        ttfb = get_ttfb_avg(string)
        keep = get_keep_rate(string)

        if rtt > 0:
            print(package, rtt, rttm, idletime, xmittime, tcp,
                  http, https, retrans, trafficvolume, ttfb, 
                  keep, sep = ',')

        subprocess.run('rm ./tmp/*', shell = True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
