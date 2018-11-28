import csv
from operator import itemgetter


IP_PROTO = {'6': 'TCP',
            '17': 'UDP'}


class FlowTiming(object):
    def __init__(self, csv_path):
        self.flow = dict()
        self.dns = dict()
        self.csv_path = csv_path
        self.host_ip = self._get_host_ip()

    def _get_host_ip(self):
        ip_counter = dict()
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                src_ip = row['ip.src']
                dst_ip = row['ip.dst']
                ip_counter[src_ip] = ip_counter.get(src_ip, 0) + 1
                ip_counter[dst_ip] = ip_counter.get(dst_ip, 0) + 1
        return max(ip_counter.items(), key=itemgetter(1))[0]

    def get_flow_timing(self):
        if len(self.flow) > 0:
            return self.flow
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                proto = row['ip.proto']
                if IP_PROTO[proto] == 'UDP':
                    self._update_udp(row)
                elif IP_PROTO[proto] == 'TCP':
                    self._update_tcp(row)

        rdns = self._get_rdns()
        for key in self.flow.keys():
            item = self.flow[key]
            key_ip = key.split(':')[0]
            if key_ip in rdns.keys():
                item['domainLookupStart'] = rdns[key_ip]['domainLookupStart']
                item['domainLookupEnd'] = rdns[key_ip]['domainLookupEnd']
            self.flow[key] = item

        return self.flow

    def _update_udp(self, row):
        time_relative = row['frame.time_relative']
        src_port = row['udp.srcport']
        dst_port = row['udp.dstport']
        qry_name = row['dns.qry.name']
        if src_port != '53' and dst_port != '53':
            return
        if qry_name not in self.dns.keys():
            self.dns[qry_name] = dict()
        if dst_port == '53':
            self.dns[qry_name]['domainLookupStart'] = time_relative
        if src_port == '53':
            aname = row['dns.a']
            self.dns[qry_name]['domainLookupEnd'] = time_relative
            self.dns[qry_name]['aname'] = aname.split(',')

    def _update_tcp(self, row):
        time_relative = row['frame.time_relative']
        src_port = row['tcp.srcport']
        dst_port = row['tcp.dstport']
        syn = row['tcp.flags.syn']
        ack = row['tcp.flags.ack']
        fin = row['tcp.flags.fin']
        cipher = row['ssl.change_cipher_spec']
        tcp_key = self._get_tcp_key(row)
        item = self.flow.get(tcp_key, dict())

        if syn == '1':
            item['connectStart'] = time_relative
        if fin == '1':
            item['connectEnd'] = time_relative
        if cipher == '1':
            if 'halfSecureConnectionStart' not in item.keys():
                item['halfSecureConnectionStart'] = time_relative
            else:
                item['secureConnectionStart'] = item['halfSecureConnectionStart']

        if (tcp_key.split(':')[1]).split('-')[0] == '80':
            if 'connectStart' in item.keys():
                if 'requestStart' not in item.keys():
                    item['requestStart'] = time_relative
                else:
                    if 'responseStart' not in item.keys():
                        item['responseStart'] = time_relative
                    else:
                        item['responseEnd'] = time_relative
        elif (tcp_key.split(':')[1]).split('-')[0] == '443':
            if 'connectStart' in item.keys():
                if ('secureConnectionStart' in item.keys() and
                        'requestStart' not in item.keys()):
                    item['requestStart'] = time_relative
                elif 'secureConnectionStart' in item.keys():
                    if 'responseStart' not in item.keys():
                        item['responseStart'] = time_relative
                    else:
                        item['responseEnd'] = time_relative
        self.flow[tcp_key] = item

    def _get_tcp_key(self, row):
        src_ip = row['ip.src']
        src_port = row['tcp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['tcp.dstport']
        if src_ip != self.host_ip:
            return '{0}:{1}-{2}'.format(src_ip, src_port, dst_port)
        else:
            return '{0}:{1}-{2}'.format(dst_ip, dst_port, src_port)

    def _get_rdns(self):
        rdns = dict()
        for key in self.dns.keys():
            item = self.dns[key]
            for aname in item['aname']:
                rdns[aname] = {'domainLookupStart': item['domainLookupStart'],
                               'domainLookupEnd': item['domainLookupEnd']}
        return rdns
