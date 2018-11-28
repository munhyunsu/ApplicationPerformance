import csv

from operator import itemgetter

from modules.pcap_to_csv import PcapToCSV
from modules.flow_timing import FlowTiming

TIMING_ORDER = ['domainLookupStart', 'domainLookupEnd',
                'connectStart', 'connectEnd',
                'secureConnectionStart', 'requestStart',
                'responseStart', 'responseEnd']


def export_pcap_timing(pcap_path, csv_path):
    pcap_reader = PcapToCSV(pcap_path)
    flow_timer = FlowTiming(pcap_reader.get_csv_path())
    flow = flow_timer.get_flow_timing()
    result = list()

    for key in flow.keys():
        item = flow[key]
        draw = dict()
        draw['key'] = key
        for timing in TIMING_ORDER:
            draw[timing] = item.get(timing, 0.0)
        result.append(draw)
        print(item, draw)

    result.sort(key=itemgetter('key'))

    with open(csv_path, 'w') as f:
        fieldnames = ['key'] + TIMING_ORDER
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(result)
