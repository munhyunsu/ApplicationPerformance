import os
import re
import statistics
import subprocess


def _clear_tmp():
    if os.path.exists('./tmp'):
        subprocess.run(['rm', '-rf', './tmp'])

def _make_tmp():
    os.makedirs('./tmp', exist_ok=True)

def get_tcptrace_output(path):
    proc = subprocess.run(['tcptrace', '--output_dir=./tmp',
                           '-lrZ', path],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL,
                          universal_newlines=True)
    return proc.stdout

def get_tcp_len(trace):
    length = len(re.findall('TCP connection', trace))
    return length

def get_trafficvolume_sum(trace):
    sumation = sum(map(int,
                       re.findall('unique bytes sent:(?:\s)+(\d+)',
                                  trace)))
    return sumation

def get_rtt_avg(trace):
    try:
        mean = statistics.mean(map(float,
                                   re.findall('RTT avg:(?:\s)+(\d+.\d+) ms',
                                              trace)))
        return mean
    except statistics.StatisticsError:
        return None

def get_rtt_max(trace):
    try:
        rtt_max = max(map(float,
                          re.findall('RTT avg:(?:\s)+(\d+.\d+) ms',
                                     trace)))
        return rtt_max
    except ValueError:
        return None

def update_pcap(path):
    _clear_tmp()
    _make_tmp()

    trace = get_tcptrace_output(path)
    data = {'connections': get_tcp_len(trace),
            'trafficvolume': get_trafficvolume_sum(trace),
            'rtt': get_rtt_avg(trace),
            'rttm': get_rtt_max(trace)}

    return data

