#!/usr/bin/env python3

import settings # Global variable module

import socket
import time

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

        for key in self.tcpdict.keys():
            mts = set()
            for timestamp, pkt in self.tcpdict[key]:
                mts.add(timestamp)
            started_date_time = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                    time.gmtime(int(min(mts))))
            times = int((max(mts)-min(mts))*100)
            pkt = (self.tcpdict[key][0][1])
            eth = dpkt.ethernet.Ethernet(pkt)
            ip = eth.data
            tcp = ip.data
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
            timing = {
                'blocked': -1,
                'dns': -1,
                'connect': -1,
                'send': 20,
                'wait': 30,
                'receive': 25,
                'ssl': -1,
            }
            self.entries.append({'startedDateTime': started_date_time,
                            'time': times,
                            'request': request,
                            'response': response,
                            'cache': {},
                            'timings': timing})

def request_from_pkt(pkt):
    pass

def response_from_pkt(pkt):
    pass

def timing_from_pkt(pkt):
    pass
