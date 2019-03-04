import sys
import csv

from file_util import get_files, parse_xml_log, parse_top_log
from image_util import get_ssim, is_white
from pcap_util import PcapToCSV, parse_pcap_csv


def get_cs(top_path, apps):
    for key in apps.keys():
        files = get_files(top_path + key)
        item = apps[key]
        top_t = dict()
        for path in files:
            sec = int((path.split('/')[-1]).split('.')[0])
            tv = parse_top_log(path)
            top_t[sec] = tv
        l = list()
        for key in top_t.keys():
            l.append((key, top_t[key]))
        l.sort()
        print(l)


def get_ll(xml_path, apps):
    for key in apps.keys():
        files = get_files(xml_path + key)
        item = apps[key]
        cuts_t = dict()
        for path in files:
            sec = int((path.split('/')[-1]).split('.')[0])
            ln = parse_xml_log(path)
            cuts_t[sec] = ln
        l = list()
        for key in cuts_t.keys():
            l.append((key, cuts_t[key]))
        l.sort()
        print(l)

get_ll('/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-a5-wlan-runtime/xml/', {'com.supercell.clashroyale': []})
# get_cs('/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-a5-wlan-init/top/', {'com.netflix.mediaclient': []})
# get_cs('/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-a5-wlan-init/top/', {'com.facebook.katana': []})
# get_ll('/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-a5-wlan-init/xml/', {'com.netflix.mediaclient': []})
# get_ll('/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-a5-wlan-init/xml/', {'com.facebook.katana': []})