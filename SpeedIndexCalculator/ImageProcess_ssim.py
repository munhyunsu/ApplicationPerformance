from PIL import Image, ImageChops
from skimage import io
from skimage.measure import compare_ssim as ssim

import csv
import os
import subprocess
from math import sqrt
import scipy.integrate as integrate
import sys
import logging
import logging.config
import xml.etree.ElementTree as ET
from operator import itemgetter

XMLDIR = '/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-s9-wlan-init/xml/'
MP4DIR = '/home/harny/Github/ApplicationPerformance/MobileUIAutomator/181211-s9-wlan-init/mp4/'
TEMPDIR = './temp/'
OUTPUTDIR = './output/'

FPS = 1


def color_based(image1, image2):
    """
    두개의 이미지pixel배열을 인자로 받아서 두개의 유사도가 얼마정도 되는지 반환
    반환값은 0 ~ 1 사이이고 유사도가 높을수록 1에 가깝다.
    image1 : 비교 첫번째 Image.getdata()
    image2 : 비교 두번째 Image.getdata()
    """
    similarity_list = []

    for array_index in range(len(image1)):
        rgb_array1 =  image1[array_index]
        rgb_array2 =  image2[array_index]

        red = pow(rgb_array1[0] - rgb_array2[0], 2)
        green = pow(rgb_array1[1] - rgb_array2[1], 2)
        blue = pow(rgb_array1[2] - rgb_array2[2], 2)

        distance = sqrt(red + green + blue)
        distance = 1/(1+sqrt(red+green+blue))
        similarity_list.append(distance)

    average_similarity = round(sum(similarity_list) / len(similarity_list), 2)

    return average_similarity


def get_split_point(files_list, cut_point):
    list_split_point = list()
    for index in range(0, len(cut_point)):
        from_index = 0
        if index > 0:
            from_index = cut_point[index-1]*FPS ## 10
        to_index = cut_point[index]*FPS ## 10

        for index in range(to_index, from_index, -1):
            if index-1 == from_index:
                list_split_point.append((from_index, index))
                break
            image1 = io.imread(files_list[index])
            image2 = io.imread(files_list[index-1])
            similarity = ssim(image1, image2, multichannel=True)
            if similarity < 0.9:
                list_split_point.append((from_index, index))
                break
    return list_split_point


def get_speed_index(files_list, list_split_point):
    speed_index = list()
    for from_index, to_index in list_split_point:
        speed = 0
        sim_list = list()
        for snaps in files_list[from_index:to_index]:
            image1 = io.imread(snaps)
            image2 = io.imread(files_list[to_index])
            similarity = (1-ssim(image1, image2, multichannel=True))*(1000/FPS)
            sim_list.append(similarity)
            speed = speed + similarity
        speed_index.append((speed, sim_list))
    return speed_index


def run_ffmpeg(video_name):
    """
    비디오 파일 이름을 입력으로 받아서 ffmpeg를 실행시켜 초단위로 이미지를 생성하여 반환
    """
    # mp4파일 이름으로 디렉토리 생성
    try:
        os.makedirs(TEMPDIR + str(video_name), exist_ok = True)
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)
        raise e

    # ffmpeg 실행
    # LuHa: fps=2 로 변경
    # command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.mp4 -vf fps=10 ' + TEMPDIR + str(video_name) + '/out%04d.jpg'
    command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.mp4 -vf fps={0} '.format(FPS) + TEMPDIR + str(video_name) + '/out%04d.jpg'
    try:
        ffmpeg = subprocess.check_call(command, stdout=subprocess.PIPE, shell=True)
    except Exception as e:
        print(e)
        raise e

    return True


def list_mp4(path):
    result = []
    for f in os.listdir(path):
        if f.endswith('.mp4'):
            result.append(f.split('.mp4')[0])
    return result


def list_jpg(path):
    result = []
    for f in os.listdir(path):
        if f.endswith('.jpg'):
            result.append(path + f)
    return result


def get_similarity_list(files_list):
    list_similarity = []

    for index in range(len(files_list)):
        try:
            image1 = io.imread(files_list[index])
            image2 = io.imread(files_list[index+1])
        except OSError as e:
            continue
        except IndexError as e:
            continue
        similarity = ssim(image1, image2, multichannel = True)
        list_similarity.append((files_list[index], files_list[index+1], similarity))

    return list_similarity


def write2csv(video_name, list_split_point, speed_list):
    with open(OUTPUTDIR+'speedindex.csv', 'a') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for index in range(0, len(speed_list)):
            writer.writerow([video_name, list_split_point[index], speed_list[index][0], speed_list[index][1]])


def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    bounds = list()
    for item in it:
        size = size+1
    return size


def get_cut_point(path):
    dir_queue = list()

    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                dir_queue.append(entry.path)

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


def main():

    mp4_list = list_mp4(MP4DIR)

    os.makedirs(TEMPDIR, exist_ok = True)
    os.makedirs(OUTPUTDIR, exist_ok = True)

    cut_point = get_cut_point(XMLDIR)

    for video_name in mp4_list:
        try:
            if not(run_ffmpeg(video_name)):
                raise Exception
        except Exception as e:
            logging.error(video_name + ' : run_ffmpeg error')
            continue
        files_list = list_jpg(TEMPDIR+video_name+'/')
        files_list.sort()

        # print(cut_point[video_name])
        list_split_point = get_split_point(files_list, cut_point[video_name])
        # print(list_split_point)
        speed_list = get_speed_index(files_list, list_split_point)
        # print(speed_list)
        write2csv(video_name, list_split_point, speed_list)


if __name__ == '__main__':
    main()
