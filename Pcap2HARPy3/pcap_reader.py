#!/usr/bin/env python3


import settings

import dpkt

from tcp_flow_builder import TCPFlowBuilder
from udp_flow_builder import UDPFlowBuilder




class PacketDispatcher(object):
    def __init__(self):
        self.tcp = list()
        self.udp = list()
        self.tcp_count = 1
        self.udp_count = 1

    def add(self, timestamp, pkt):
        eth = dpkt.ethernet.Ethernet(pkt)
        if isinstance(eth.data, dpkt.ip.IP):
            ip = eth.data
            if isinstance(ip.data, dpkt.tcp.TCP):
                #print('TCP count {0}:'.format(self.tcp_count))
                self.tcp_count = self.tcp_count + 1
                self.tcp.append((timestamp, pkt))
            elif isinstance(ip.data, dpkt.udp.UDP):
                #print('UDP count {0}:'.format(self.udp_count))
                self.udp_count = self.udp_count + 1
                self.udp.append((timestamp, pkt))

    def finish(self):
        self.tcp.finish()
        


class PcapReader(object):
    def __init__(self, input_path):
        self.input_path = input_path
        
        pcap_file = open(self.input_path, 'rb')
        pcap = dpkt.pcap.Reader(pcap_file)

        dispatcher = PacketDispatcher()
        pcap.dispatch(0, dispatcher.add)

        self.tcp = dispatcher.tcp
        self.udp = dispatcher.udp
