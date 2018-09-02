import os
import sys
import shutil
import csv
import subprocess
import datetime
import xml.etree.ElementTree as ET
import random
import re


def check_binary(binaries):
    for binary in binaries:
        if shutil.which(binary) is None:
            raise FileNotFoundError


def command_popen(command):
    return subprocess.Popen(command, shell=True)


def command_check(command):
    return subprocess.check_call(command, shell=True)


def command_output(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def send_ping():
    command = 'adb shell su -c ping -c 1 -w 1 -I wlan0 127.0.0.1'
    return command_popen(command)


def terminate_ping(ping_proc):
    try:
        ping_proc.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        ping_proc.kill()
        ping_proc.communicate()


def get_second_from_start(start_time):
    return (start_time - datetime.datetime.now()).total_seconds()


def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    bounds = list()
    for item in it:
        size = size+1
        if item.get('clickable') == 'true':
            bounds.append(item.get('bounds'))

    choose = random.choice(bounds)
    axes = re.findall('\d+', choose)
    point = (random.randrange(int(axes[0]), int(axes[2])),
             random.randrange(int(axes[1]), int(axes[3])))
    return size, point


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
    app_list = list()
    with open('app_list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['package_name'])
            app_list.append(row['package_name'])
    package_name = app_list[0]

    # clear cache without user data
    # adb shell pm clear APKNAME
    # adb shell run-as APKNAME rm -rf /data/data/APKNAME/cache/*
    # adb shell su - c rm - rf /data/data/com.amazon.mShop.android.shopping/cache/*
    command = 'adb shell su -c rm -rf /data/data/{0}/cache/*'.format(package_name)
    command_check(command)

    # execute tcpdump
    command = 'adb shell su -c tcpdump -i wlan0 -w /sdcard/{0}.pcap -s 0'.format(package_name)
    tcpdump_proc = command_popen(command)

    # execute screenrecord
    command = 'adb shell screenrecord /sdcard/{0}.mp4'.format(package_name)
    screenrecord_proc = command_popen(command)

    # launch app
    start_time = datetime.datetime.now()
    ping_proc = send_ping()
    command = 'adb shell monkey -p {0} -c android.intent.category.LAUNCHER 1'.format(package_name)
    command_check(command)
    terminate_ping(ping_proc)

    # insert event
    for index in range(0, 5):
        # export XML log
        dump_time = get_second_from_start(start_time)
        command = 'adb shell uiautomator dump /sdcard/xml/{0}.xml'.format(dump_time)
        dump_output = command_output(command)
        if not dump_output.startswith('UI hierchary dumped to:'):
            continue
        # pull XML log
        command = 'adb pull /sdcard/xml/{0}.xml ./{1}/xml/'.format(dump_time, package_name)
        command_check(command)





    # terminate tcpdump
    tcpdump_proc.terminate()

    # terminate screenrecord
    screenrecord_proc.terminate()

if __name__ == '__main__':
    main()