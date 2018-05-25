#!/usr/bin/env python3

import settings # Global variable module

import socket
import time
import re
import datetime
import subprocess

import dpkt

class Session(object):
    def __init__(self, pcapreader):
        self.pcapreader = pcapreader
        self.entries = list()
        
        self.tcpdict = dict()
        self.udpdict = dict()

        for timestamp, pkt in self.pcapreader.tcp:
            eth = dpkt.ethernet.Ethernet(pkt)
            ip = eth.data
            tcp = ip.data
            direction1 = ((ip.src, tcp.sport), (ip.dst, tcp.dport))
            direction2 = ((ip.dst, tcp.dport), (ip.src, tcp.sport))
            if direction1 in self.tcpdict:
                direction = direction2
            elif direction2 in self.tcpdict:
                direction = direction1
            else:
                direction = direction1
            if direction in self.tcpdict:
                self.tcpdict[direction].append((timestamp, pkt))
            else:
                self.tcpdict[direction] = [(timestamp, pkt)]

        for timestamp, pkt in self.pcapreader.udp:
            eth = dpkt.ethernet.Ethernet(pkt)
            ip = eth.data
            udp = ip.data
            direction1 = ((ip.src, udp.sport), (ip.dst, udp.dport))
            direction2 = ((ip.dst, udp.dport), (ip.src, udp.sport))
            if direction1 in self.udpdict:
                direction = direction2
            elif direction2 in self.udpdict:
                direction = direction1
            else:
                direction = direction1
            if direction in self.udpdict:
                self.udpdict[direction].append((timestamp, pkt))
            else:
                self.udpdict[direction] = [(timestamp, pkt)]

        string = get_tcptrace(settings.input)
        (date_result, url_result, byte_result, send_result, wait_result, receive_result) = forming_tcptrace(string)
        print(len(date_result), len(url_result), len(byte_result), len(send_result), len(wait_result), len(receive_result))


        for index in range(0, len(date_result)):
            request = {
                'method': 'GET',
                'url': url_result[index],
                'httpVersion': 'HTTP/1.1',
                'cookies': [],
                'headers': [],
                'queryString': [],
                'headersSize': 20,
                'bodySize': -1
            }
            response = {
                'status': 200,
                'statusText': 'OK',
                'httpVersion': 'HTTP/1.1',
                'cookies': [],
                'headers': [],
                'content': {
                    'size': byte_result[index],
                    'mimeType': 'application/x-www-form-urlencoded'
                },
                'redirectURL': '',
                'headersSize': 20,
                'bodySize': -1,
            }
            timing = {
                'blocked': -1,
                'dns': -1,
                'connect': -1,
                'send': send_result[index],
                'wait': wait_result[index],
                'receive': receive_result[index],
                'ssl': -1,
            }
            self.entries.append({'startedDateTime': date_result[index],
                            'time': send_result[index] + wait_result[index] + receive_result[index],
                            'request': request,
                            'response': response,
                            'cache': {},
                            'timings': timing})


def get_tcptrace(input_file):
    cp = subprocess.run(['tcptrace', '-lnr', input_file],
                        stdout = subprocess.PIPE,
                        stderr = subprocess.DEVNULL,
                        universal_newlines = True)

    return cp.stdout


def forming_tcptrace(string):
    date = re.findall('first packet:(?:\s)+([^\n]+)', string)
    date_result = list()
    for row in date:
        d = datetime.datetime.strptime(row, '%a %b %d %H:%M:%S.%f %Y')
        date_result.append(d.strftime('%Y-%m-%dT%H:%M:%S+09:00'))

    url = re.findall('host (?:\w+:\s+)([\d.:]+)', string)
    url_result = list()
    for row in url[1::2]:
        url_result.append(row.split(':')[0])

    byte = re.findall('unique bytes sent:(?:\s)+(\d+)', string)
    byte_result = list()
    for index in range(0, len(byte), 2):
        byte_result.append(int(byte[index]) + int(byte[index+1]))

    send = re.findall('data xmit time:(?:\s)+(\d+.\d+) secs', string)
    send_result = list()
    receive_result = list()
    for index in range(0, len(send), 2):
        send_result.append(int(float(send[index])*1000))
        receive_result.append(int(float(send[index+1])*1000))

    wait = re.findall('idletime max:(?:\s)+(\d+.\d+|NA) ms', string)
    wait_result = list()
    for index in range(0, len(wait), 2):
        if wait[index] == 'NA':
            one = 0
        else:
            one = int(float(wait[index]))
        if wait[index+1] == 'NA':
            two = 0
        else:
            two = int(float(wait[index+1]))
        wait_result.append((one + two)//len(date_result))

    return (date_result, url_result, byte_result, send_result, wait_result, receive_result)


def request_from_pkt(pkt):
    request = {
        'method': 'GET',
        'url': socket.inet_ntoa(ip.dst),
        'httpVersion': 'HTTP/1.1',
        'cookies': [],
        'headers': [],
        'queryString': [],
        'headersSize': tcp.off*4,
        'bodySize': -1
    }
    pass

def response_from_pkt(pkt):
    response = {
        'status': 200,
        'statusText': 'OK',
        'httpVersion': 'HTTP/1.1',
        'cookies': [],
        'headers': [],
        'content': {
            'size': ip.len - (tcp.off*4),
            'mimeType': 'application/x-www-form-urlencoded'
        },
        'redirectURL': '',
        'headersSize': tcp.off*4,
        'bodySize': -1,
    }
    pass

def timing_from_pkt(pkt):
    timing = {
        'blocked': -1,
        'dns': -1,
        'connect': -1,
        'send': 20,
        'wait': 30,
        'receive': 25,
        'ssl': -1,
    }
    pass
