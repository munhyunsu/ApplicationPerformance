import csv
import unittest

from modules.pcap_to_csv import PcapToCSV
from modules.flow_timing import FlowTiming

PCAP_PATH = 'tests/http.pcap'


class FlowTimingTests(unittest.TestCase):
    def setUp(self):
        pcap_reader = PcapToCSV(PCAP_PATH)
        self.flow_timing = FlowTiming(pcap_reader.get_csv_path())

    def test__get_host_ip(self):
        self.assertEqual('145.254.160.237', self.flow_timing._get_host_ip())
