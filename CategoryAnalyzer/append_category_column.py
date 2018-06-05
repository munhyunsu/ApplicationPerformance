#!/usr/bin/env python3

import sys
import csv
import sqlite3

INPUTFILE = 'traffic.csv'
BASEDB = '/home/harny/SharedFolder/appdb.sqlite'
OUTPUTFILE = 'category.csv'


def main(argv = sys.argv):
    # inputs
    f = open(INPUTFILE, 'r')
    reader = csv.DictReader(f)
    conn = sqlite3.connect(BASEDB)
    c = conn.cursor()

    # outputs
    f2 = open(OUTPUTFILE, 'w')
    fieldnames = ['package', 'SpeedIndex', 'RTT', 'Connections', 
                  'TrafficVolume', 'TTFB', 'Retransmit', 'Layout', 
                  'Ads', 'Image', 'Category']
    writer = csv.DictWriter(f2, fieldnames = fieldnames)
    writer.writeheader()

    query = 'SELECT category FROM list WHERE package = ?'
    for row in reader:
        c.execute(query, (row['package'],))
        category = c.fetchone()[0]
        writer.writerow({'package': row['package'],
                         'SpeedIndex': row['SpeedIndex'],
                         'RTT': row['RTT'], 
                         'Connections': row['Connections'],
                         'TrafficVolume': row['TrafficVolume'], 
                         'TTFB': row['TTFB'],
                         'Retransmit': row['Retransmit'],
                         'Layout': row['Layout'], 
                         'Ads': row['Ads'],
                         'Image': row['Image'],
                         'Category': category})
        
    conn.close()

if __name__ == '__main__':
    sys.exit(main())
