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

INPUTDIR = '/home/harny/SharedFolder/Mobile/180415/record2/'
INPUTDIR2 = '/home/harny/SharedFolder/Mobile/180415/record3/'
OUTPUTDIR = '/home/harny/SharedFolder/Mobile/180415/video2/'


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


def get_split_point(input_list):

    list_split_point = []
    temp = 0
    temp_index = 0
    for index in range(len(input_list)):
        if input_list[index][2] >= 0.8:
            if input_list[index][2] >= temp:
                temp = input_list[index][2]
                temp_index = index
            else:
                temp = 0.8
                temp_index = index

        else:
            if temp != 0:
                list_split_point.append(temp_index)
                temp = 0
    list_split_point.append(len(input_list)-1)
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
    intevel = 1
    latest_index = 0
    list_speed = []
    sum_of_speed = 0
    for split_point in list_split_point:
        speed_index = []
        for index in range(latest_index, split_point+1):
            if(list_similarity[index][2] >= 0.8): #남은 여유시간 제거
                continue
            speed_index.append(list_similarity[index][1].split('.jpg')[0][-3:])
            sum_of_speed += intevel * (1 - list_similarity[index][2])
        list_speed.append([speed_index, sum_of_speed])
        sum_of_speed = 0
        latest_index = split_point+1
    return list_speed


def run_ffmpeg(video_name):
    """
    비디오 파일 이름을 입력으로 받아서 ffmpeg를 실행시켜 초단위로 이미지를 생성하여 반환
    """
    # mp4파일 이름으로 디렉토리 생성
    try:
        os.makedirs(OUTPUTDIR + str(video_name), exist_ok = True)
    except FileExistsError as e:
        print (e)
    except Exception as e:
        print(e)
        raise e

    # ffmpeg 실행
    # LuHa: fps=2 로 변경
    command = 'ffmpeg -i ' + INPUTDIR+str(video_name) + '.mp4 -vf fps=10 ' + OUTPUTDIR+str(video_name) + '/out%03d.jpg'
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
        list_similarity.append([files_list[index], files_list[index+1], similarity])

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

def main():

    mp4_list = list_mp4(INPUTDIR)

    os.makedirs(INPUTDIR2, exist_ok = True)
    os.makedirs(OUTPUTDIR, exist_ok = True)

    for video_name in mp4_list:
        try:
            if not(run_ffmpeg(video_name)):
                raise Exception
        except Exception as e:
            logging.error(video_name + ' : run_ffmpeg error')
            continue

        files_list = list_jpg(OUTPUTDIR+video_name+'/')
        files_list.sort()

        """
        list_similarity = get_similarity_list(files_list)
        logging.info(video_name + ' list_similarity : ' + list_similarity)
        list_split_point = get_split_point(list_similarity)
        logging.info(video_name + ' list_split_point : ' + list_split_point)
        speed_list = get_speed_index(list_similarity, list_split_point)
        logging.info(video_name + ' speed_list : ' + speed_list)
        write2csv(video_name, speed_list)
        """

        list_similarity = get_similarity_list(files_list)
        # list_similarity_last = get_similarity_list_last(files_list)
        # print(list_similarity_last)
        logging.info(video_name + ' list_similarity : ' + str(list_similarity))
        speed_list = get_speed_index_of_first_activity(list_similarity)
        logging.info(video_name + ' speed_list : ' + str(speed_list))
        write2csv(video_name, speed_list)

        os.rename(INPUTDIR+video_name+'.mp4', INPUTDIR2+video_name+'.mp4')


if __name__ == '__main__':
    main()
