import os
import sys
import csv

from analyzer_pcap import update_pcap

ARGS = None


def main():
    result = list()
    with open(ARGS.info, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data = {'package': row[0],
                    'SI': row[1],
                    'FP': row[2],
                    'LL': row[3],
                    'CS': row[4],
                    'RT': row[5]}
            pcap_path = os.path.join(os.path.abspath(ARGS.pcap),
                                     '{0}.pcap'.format(row[0]))
            pcap_data = update_pcap(pcap_path)
            data.update(pcap_data)
            result.append(data)
    if os.path.exists(ARGS.output):
        mode = 'a'
    else:
        mode = 'w'
    with open(ARGS.output, mode) as f:
        fieldnames = ['package', 'connections', 'trafficvolume',
                      'rtt', 'rttm',
                      'SI', 'FP', 'LL', 'CS', 'RT']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(result)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pcap',
                         type=str,
                         required=True,
                         help='root directory of pcap')
    #parser.add_argument('-x', '--xml',
    #                     type=str,
    #                     required=True,
    #                     help='root directory of xml')
    parser.add_argument('-i', '--info',
                         type=str,
                         required=True,
                         help='result file about SI,FP,LL,CS,RT')
    parser.add_argument('-o', '--output',
                         type=str,
                         required=True,
                         help='output file location')
    ARGS = parser.parse_args()

    main()

