import unittest


from modules.pcap_to_csv import PcapToCSV

PCAP_PATH = 'tests/http.pcap'


class PcapToCSVTests(unittest.TestCase):
    def setUp(self):
        self.pcap_reader = PcapToCSV(PCAP_PATH)

    def test_get_csv_path(self):
        self.assertEqual('tests/http.csv', self.pcap_reader.csv_path)
