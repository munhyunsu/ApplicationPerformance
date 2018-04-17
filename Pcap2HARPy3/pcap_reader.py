#!/usr/bin/env python3


import settings

from tcp_flow_builder import TCPFlowBuilder
from udp_flow_builder import UDPFlowBuilder


class PacketDispatcher(object):
    def __init__(self):
        self.tcpflow = TCPFlowBuilder()
        self.udpflow = UDPFlowBuilder()

class PcapReader(object):
    def __init__(self, path):
        self.path = path
        dispatcher = PacketDispatcher()
        print('pcap reader init')
