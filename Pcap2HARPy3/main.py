#!/usr/bin/env python3

import sys

import argparse


import settings # Global variable module
from pcap_reader import PcapReader
from har_session import Session

def main(argv = sys.argv):
    print('Packet Capture to HTTP Archive Ver. 3')

    pcapreader = PcapReader(path = settings.input)

    sessions = Session(pcapreader = pcapreader)

    print('Main settings:', settings.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Converts PCAP to HAR')
    parser.add_argument('-n', '--no-pages', 
                        action = 'store_false', 
                        dest = 'pages')
    parser.add_argument('-d', '--drop-bodies',
                        action = 'store_true', 
                        dest = 'drop_bodies')
    parser.add_argument('-k', '--keep-unfulfilled-requests', 
                        action = 'store_true', 
                        dest = 'keep_unfulfilled')
    parser.add_argument('-r', '--resource-usage',
                        action = 'store_true', 
                        dest = 'resource_usage')
    parser.add_argument('-p', '--pad-missing-tcp-data',
                        action = 'store_true', 
                        dest = 'pad_missing_tcp_data')
    parser.add_argument('-s', '--strict-http-parsing',
                        action = 'store_true',
                        dest = 'strict_http_parsing')
    parser.add_argument('-l', '--log',
                        action = 'store',
                        dest = 'logfile',
                        default = 'pcap2harv3.log')
    parser.add_argument('-i', '--input',
                        action = 'store',
                        dest = 'input',
                        required = True)
    parser.add_argument('-o', '--output',
                        action = 'store',
                        dest = 'output')
    options = parser.parse_args()
    
    settings.pages = options.pages
    settings.drop_bodies = options.drop_bodies
    settings.keep_unfulfilled = options.keep_unfulfilled
    settings.resource_usage = options.resource_usage
    settings.pad_missing_tcp_data = options.pad_missing_tcp_data
    settings.strict_http_parsing = options.strict_http_parsing
    settings.logfile = options.logfile
    settings.input = options.input
    settings.output = options.input + '.har'
    if options.output != None:
        settings.output = options.output

    sys.exit(main())
