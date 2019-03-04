import os
import csv
import copy
import subprocess

from pcap_processor import export_pcap_timing


def get_nintynine(csv_path):
    volume = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                volume = volume + int(row.get('ip.len', 0))
            except ValueError:
                pass

    return volume * 0.99


def get_nintynine_time(csv_path, thresh):
    volume = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                volume = volume + int(row.get('ip.len', 0))
            except ValueError:
                pass
            if volume > thresh:
                return row.get('frame.time_relative')


def get_traffic_volume(csv_path):
    volume = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                volume = volume + int(row.get('ip.len', 0))
            except ValueError:
                pass
    return volume


def main():
    target = '181211-s9-wlan-init'

    os.makedirs('./output', exist_ok=True)
    with os.scandir('/home/harny/Github/ApplicationPerformance/MobileUIAutomator/{0}/pcap'.format(target)) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file() and entry.name.endswith('.pcap'):
                try:
                    export_pcap_timing(entry.path, './output/{0}.csv'.format(entry.name))
                except:
                    continue
                result = dict()
                with open('./output/{0}.csv'.format(entry.name), 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sample = dict()
                        sample['dns'] = float(row.get('domainLookupEnd', 0.0)) - float(
                            row.get('domainLookupStart', 0.0))
                        sample['connect'] = float(row.get('secureConnectionStart', 0.0)) - float(
                            row.get('connectStart', 0.0))
                        sample['secure'] = float(row.get('requestStart', 0.0)) - float(
                            row.get('secureConnectionStart', 0.0))
                        sample['request'] = float(row.get('responseStart', 0.0)) - float(row.get('requestStart', 0.0))
                        sample['response'] = float(row.get('responseEnd', 0.0)) - float(row.get('responseStart', 0.0))
                        sample['quic'] = float(row.get('quicConnectEnd', 0.0)) - float(row.get('quicConnectStart', 0.0))
                        for key in sample.keys():
                            if sample[key] > 0:
                                result[key] = result.get(key, 0) + sample[key]
                total = 0
                for key in result:
                    total = total + result[key]
                for key in result.keys():
                    result[key] = result[key] / total
                result['name'] = entry.name

                csv_path = '/home/harny/Github/ApplicationPerformance/MobileUIAutomator/{0}/pcap/{1}.csv'.format(target, entry.name[:-5])
                result['nintynine'] = get_nintynine_time(csv_path, get_nintynine(csv_path))
                result['trafficvolume'] = get_traffic_volume(csv_path)

                if os.path.exists('./{0}.csv'.format(target)):
                    with open('./{0}.csv'.format(target), 'a') as f:
                        fieldnames = ['name', 'dns', 'connect', 'secure', 'request', 'response', 'quic', 'nintynine', 'trafficvolume']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerow(result)
                else:
                    with open('./{0}.csv'.format(target), 'w') as f:
                        fieldnames = ['name', 'dns', 'connect', 'secure', 'request', 'response', 'quic', 'nintynine', 'trafficvolume']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(result)


if __name__ == '__main__':
    # main()
    export_pcap_timing('./com.google.android.youtube.pcap', './com.google.android.youtube.pcap.csv')

