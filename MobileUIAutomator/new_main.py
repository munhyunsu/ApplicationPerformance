import os
import sys
import shutil
import csv


def check_binary(binaries):
    for binary in binaries:
        if shutil.which(binary) is None:
            raise FileNotFoundError


def main(argv=sys.argv):
    if len(argv) < 1:
        print('Can not reached line')
        os.exit(0)
    # Check binaries
    binaries = ['adb']
    check_binary(binaries)

    # Get list of target apps
    if not os.path.exists('app_list.csv'):
        raise Exception('Need app_list.csv')
    with open('app_list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['package_name'])

    # execute tcpdump

    #




if __name__ == '__main__':
    main()