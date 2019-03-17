import os
import shlex
import xml.etree.ElementTree as ET
import subprocess

from util.path import std_path


FPS = 10

def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    bounds = list()
    for item in it:
        size = size+1
    return size
    

def get_cut(path):
    dir_queue = list()

    # directory handling
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                dir_queue.append(entry.path)

    # find cut-point
    cut_point = dict()
    for inner_path in dir_queue:
        cuts_t = list()
        with os.scandir(inner_path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    sec = int((entry.name.split('/')[-1]).split('.')[0])
                    ln = parse_xml_log(entry.path)
                    cuts_t.append((sec, ln))
        cuts_t.sort(key=itemgetter(0))

        cuts = list()
        dup = 0
        dup_c = 0
        for sec, ln in cuts_t:
            if dup == ln:
                dup_c = dup_c + 1
            else:
                dup_c = 0
            dup = ln
            if dup_c >= 4:
                cuts.append(sec)
                dup_c = 0
            if (len(cuts)+1)*60 < sec:
                cuts.append(sec)
            if len(cuts) >= 5:
                break

        cut_point[inner_path.split('/')[-1]] = cuts

    return cut_point


def get_speedindex(mp4_dir, xml_dir, out_dir):
    for video in get_files(mp4_dir, ext='.mp4'):
        # make output directory by video
        output = os.path.join(out_dir, video)
        os.makedirs(output, exist_ok=True)
        
        # create snapshot of video
        command_line = 'ffmpeg -i {0} -vf fps={1} {2}/%04d.jpg'.format(
                               video, FPS, output)
        command = shlex.split(command_line)
        subprocess.check_call(command, stdout=subprocess.PIPE)

