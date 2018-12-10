from PIL import Image, ImageChops
from skimage import io
from skimage.measure import compare_ssim as ssim

import os
import subprocess
from math import sqrt
import scipy.integrate as integrate
import sys
import logging
import logging.config
import xml.etree.ElementTree as ET
from operator import itemgetter

XMLDIR = '/home/harny/Github/ApplicationPerformance/MobileUIAutomator/a5-wlan/xml/'
MP4DIR = '/home/harny/Github/ApplicationPerformance/MobileUIAutomator/a5-wlan/mp4/'
TEMPDIR = './temp/'
OUTPUTDIR = './output/'


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


def get_split_point(input_list, cut_point):

    list_split_point = list()
    for index in range(0, len(cut_point)):
        from_index = 0
        if index > 0:
            from_index = cut_point[index-1]*10
        to_index = cut_point[index]*10

        for index in range(to_index, from_index, -1):
            if input_list[index][2] >= 0.8:
                continue
            else:
                list_split_point.append((from_index, index))
                break
    return list_split_point


def get_speed_index_of_first_activity(list_similarity):
    # 리스트를 역순으로 뒤집어 액티비티 로딩 완료 후 움직이지 않는 스크린샷 제거
    list_similarity.reverse()
    last_shot_index = 0
    for index in range(len(list_similarity)):
        if list_similarity[index][2] >= 0.90:
            last_shot_index = index
        else:
            print(last_shot_index)
            last_shot_index = len(list_similarity) - last_shot_index -1
            break
    print('last_shot_index : ' + str(last_shot_index))
    # 다시 원래대로 뒤집어서 로딩완료직후까지의 speed index 구하기
    list_similarity.reverse()
    speed_index = 0
    speed_index_list = []
    for index in range(last_shot_index+1):
        speed_index_list.append(list_similarity[index][1].split('.jpg')[0][-3:])
        speed_index += (1 - list_similarity[index][2])

    return [[speed_index_list, speed_index]]


def get_speed_index(list_similarity, list_split_point):
    speed_index = list()
    for from_index, to_index in list_split_point:
        speed = 0
        for sim in list_similarity[from_index:to_index]:
            speed = speed + sim
        speed_index.append(speed)
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
    command = 'ffmpeg -i ' + MP4DIR+str(video_name) + '.mp4 -vf fps=10 ' + TEMPDIR+str(video_name) + '/out%04d.jpg'
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


def get_similarity_list_last(files_list):
    files_list = files_list[:5]
    list_similarity = []

    for index in range(len(files_list)):
        try:
            image1 = io.imread(files_list[index])
            image2 = io.imread(files_list[-1])
        except OSError as e:
            continue
        except IndexError as e:
            continue
        similarity = ssim(image1, image2, multichannel = True)
        list_similarity.append([files_list[index], files_list[-1], similarity])

    return list_similarity


def write2csv(app_name, speed_list):
    if len(speed_list) == 0:
        logging.info(app_name + ' len(speed_list) is 0')
        return
    csv = open(OUTPUTDIR+'speed_result.csv','a')

    for speed_row in speed_list:
        speed_index = speed_row[1]
        start_time = speed_row[0][0]
        end_time = speed_row[0][len(speed_row[0])-1]
        csv.write(app_name + ',' + str(start_time) + ',' + str(end_time) + ',' + str(speed_index) +'\n')
        logging.info(app_name + ',' + str(start_time) + ',' + str(end_time) + ',' + str(speed_index) +'\n')

    csv.close()


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

        list_similarity = get_similarity_list(files_list)
        list_split_point = get_split_point(list_similarity, cut_point[video_name.split('.')[0]])
        speed_list = get_speed_index(list_similarity, list_split_point)
        print(video_name, list_split_point, speed_list)


if __name__ == '__main__':
    main()
