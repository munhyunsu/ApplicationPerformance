from PIL import Image, ImageChops
from skimage import io
from skimage.measure import compare_ssim as ssim

import os
import subprocess
from math import sqrt
import sys
import logging
import logging.config

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



def col2(image1, image2):
    pass



def get_app_dirs(path):
    dir_queue = list()

    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                yield entry.path



def check_thresholds(app_dir):
    files = list()

    with os.scandir(app_dir) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                files.append(entry.path)

    files.sort()
    base = files.pop()
    base_pil = Image.open(base).getdata()
    base_ski = io.imread(base)

    for comp in files:
        comp_pil = Image.open(comp).getdata()
        comp_ski = io.imread(comp)
        print(base, comp,
              ssim(base_ski, comp_ski, multichannel = True), sep = ','
              )


def mp4_to_jpgs(mp4_dir):
    file_queue = list()

    with os.scandir(mp4_dir) as it:
        for entry in it:
            if entry.name.endswith('.mp4') and entry.is_file():
                file_queue.append(entry.path)

    for file_path in file_queue:
        # mp4/com.placartv2.app.mp4
        dir_name = file_path.split('/')[1]
        dir_name = dir_name[:-4]
        os.makedirs('./jpgs/{0}'.format(dir_name), exist_ok=True)
        command = 'ffmpeg -i {0} -vf fps=10 ./jpgs/{1}/%03d.jpg'.format(file_path, dir_name)
        subprocess.check_call(command, shell=True)


def main(argv = sys.argv):
#    mp4_to_jpgs(argv[1])
    for app_dir in get_app_dirs(argv[1]):
        check_thresholds(app_dir)



if __name__ == '__main__':
    main()
