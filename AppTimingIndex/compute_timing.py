import csv
import copy

HOST = '192.168.86.122'
FLOWS = dict()
DNS = dict()
RDNS = dict()


def get_key(value):
    if value['Source'] != HOST:
        ip = value['Source']
        port = value['SrcPort']
    else:
        ip = value['Destination']
        port = value['DstPort']
    return ':'.join([ip, port])


def update_dns(value):
    if value['DstPort'] == '53':
        info = value['Info']
        time = value['Time']
        query_domain = info.split(' ')[-1]
        DNS[query_domain] = {'domainLookupStart': time}
    elif value['SrcPort'] == '53':
        info = value['Info']
        time = value['Time']
        for key in DNS.keys():
            item = DNS[key]
            if (key in info and
                    'domainLookupEnd' not in item.keys()):
                DNS[key]['domainLookupEnd'] = time
                DNS[key]['ip'] = value['Info'].split(' ')[-1]


def update_tcp(value):
    key = get_key(value)
    item = FLOWS.get(key, dict())
    info = value['Info']
    if '[SYN]' in info:
        item['connectStart'] = value['Time']
    elif '[FIN, ACK]' in info:
        item['connectEnd'] = value['Time']
    elif 'Change Cipher Spec' in info:
        item['secureConnectionStart'] = value['Time']

    if key.split(':')[-1] == '80':
        if 'connectStart' in item.keys():
            if 'requestStart' not in item.keys():
                item['requestStart'] = value['Time']
            else:
                if 'responseStart' not in item.keys():
                    item['responseStart'] = value['Time']
                else:
                    item['responseEnd'] = value['Time']
    elif key.split(':')[-1] == '443':
        if 'connectStart' in item.keys():
            if ('secureConnectionStart' in item.keys() and
                    'requestStart' not in item.keys()):
                item['requestStart'] = value['Time']
            elif 'secureConnectionStart' in item.keys():
                if 'responseStart' not in item.keys():
                    item['responseStart'] = value['Time']
                else:
                    item['responseEnd'] = value['Time']
    FLOWS[key] = item


def get_rdns():
    for key in DNS.keys():
        item = DNS[key]
        RDNS[item['ip']] = {'domainLookupStart': item['domainLookupStart'],
                            'domainLookupEnd': item['domainLookupEnd']}


def export_csv():
    result = list()
    for key in FLOWS.keys():
        item = FLOWS[key]
        ip = key.split(':')[0]
        try:
            if ip in RDNS.keys():
                draw = dict()
                draw['key'] = key
                draw['wait1'] = RDNS[ip]['domainLookupStart']
                draw['dns'] = abs(float(RDNS[ip]['domainLookupEnd']) - float(RDNS[ip]['domainLookupStart']))
                draw['wait2'] = abs(float(item['connectStart']) - float(RDNS[ip]['domainLookupEnd']))
                draw['connect'] = abs(float(item['connectEnd']) - float(item['connectStart']))
                draw['secure'] = abs(float(item['secureConnectionStart']) - float(item['connectEnd']))
                draw['request'] = abs(float(item['requestStart']) - float(item['secureConnectionStart']))
                draw['wait3'] = abs(float(item['responseStart']) - float(item['requestStart']))
                draw['response'] = abs(float(item['responseEnd']) - float(item['responseStart']))
                result.append(draw)
                print(draw)
        except:
            continue

    with open('output.csv', 'w') as f:
        # fieldnames = ['key', 'domainLookupStart', 'domainLookupEnd', 'connectStart', 'connectEnd',
        #               'secureConnectionStart', 'requestStart', 'responseStart', 'responseEnd']
        fieldnames = ['key', 'wait1', 'dns', 'wait2', 'connect',
                      'secure', 'request', 'wait3', 'response']
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(result)


def main():
    with open('amazon.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = get_key(row)
            protocol = row['Protocol']
            if protocol == 'DNS':
                update_dns(row)
            elif protocol in ['TCP', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2']:
                update_tcp(row)

    print(DNS)
    print(FLOWS)

    get_rdns()
    export_csv()


if __name__ == '__main__':
    main()
