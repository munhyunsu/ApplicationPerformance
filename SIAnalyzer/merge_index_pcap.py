#!/usr/bin/env python3

import sys
import os
import csv

def get_si_dict(path, result = dict()):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result[row[0]] = row[3]
    return result


def get_ads_dict(path, result = dict()):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result[row[0]] = [row[1], row[2], row[3], row[4]]
    return result


def main(argv):
    sipath1 = '/home/harny/SharedFolder/Mobile/180410/video/speed_result.csv'
    sipath2 = '/home/harny/SharedFolder/Mobile/180411/video/speed_result.csv'
    sipath3 = '/home/harny/SharedFolder/Mobile/180415/video/speed_result.csv'

    sis = get_si_dict(sipath1)
    sis = get_si_dict(sipath2, sis)
    sis = get_si_dict(sipath3, sis)

    adpath = ['ad180410.csv', 'ad180411.csv', 'ad180415.csv']
    ads = dict()
    for path in adpath:
        ads = get_ads_dict(path, ads)

    tpath = ['180410.csv', '180411.csv', '180415.csv']
    print('package', 'speedindex', 'rtt', 'tcp', 'volume', 
          'ttfb', 'retrans', 'layout', 'ads', 'image', sep = ',')
    for path in tpath:
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    print(row['package'],
                          float(sis[row['package']])*100,
                          row['rtt'],
                          row['tcp'],
                          row['trafficvolume'],
                          row['ttfb'],
                          row['retrans'],
                          ads[row['package']][0],
                          ads[row['package']][2],
                          ads[row['package']][3],
                          sep = ',')
                except:
                    pass
            

if __name__ == '__main__':
    sys.exit(main(sys.argv))
