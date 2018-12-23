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
    cp = subprocess.run(['tcptrace', '-lr', path], 
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

import xml.etree.ElementTree as ET

def get_xml_size(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()

    size = 0
    for item in it:
        size = size + 1

    return size


def get_last_size(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()

    size = 0
    for item in it:
        if len(item.getchildren()) == 0:
            size = size + 1

    return size



def get_ads_size(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()

    size = 0
    for item in it:
        resource = item.get('resource-id')
        if resource == None:
            continue
        resource = resource.lower()
        if 'ad' in resource:
            size = size + 1

    return size

def get_img_size(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()

    size = 0
    for item in it:
        resource = item.get('class')
        if resource == None:
            continue
        resource = resource.lower()
        if ('img' in resource) or ('image' in resource):
            size = size + 1

    return size





def main(argv):
    path = argv[1]

    pack_max = dict()
    pack_result = dict()

    print('package', 'layouts','lastlayout','ads','img', sep=',')
    for path in get_files(path, '.xml', recursive = True):
        package = path.split('/')[-2]
        number = int((path.split('/')[-1])[:-4])
        if pack_max.get(package, 0) < number:
            pack_max[package] = number
            pack_result[package] = [get_xml_size(path), 
                                    get_last_size(path),
                                    get_ads_size(path),
                                    get_img_size(path)]

    for key in pack_result.keys():
        item = pack_result[key]
        print(key, item[0], item[1], item[2], item[3], sep = ',')



if __name__ == '__main__':
    sys.exit(main(sys.argv))
