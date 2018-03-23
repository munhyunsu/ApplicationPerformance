from device_controller import DeviceController
import configparser
import os


def list_apk(path):
    """
        path를 입력받아 해당 경로에 존재하는 apk파일들을 리스트형태로 가지고온다.
    """
    result = []
    for f in os.listdir(path):
        if f.endswith('.apk'):
            result.append(f.split('.apk')[0])
    return result

def main():

    # config.ini 설정변수 읽기
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        apk_directory = config.get('device_controller','apk_directory')
        apk_list = list_apk(apk_directory)
    except Exception as e:
        print(str(e) + ' config.ini파일 읽는중에 에러발생')
        raise e

    # DeviceController객체 생성
    controller = DeviceController()

    # 디렉토리 안에 들어있는 모든  APK파일에 대해서 진행
    for apk in apk_list:
        try:
            # APK파일 하나씩 테스트 진행
            controller.run_test(apk)
        except Exception as e:
            # 예외가 발생한다면 앱 테스팅 중지 후 다음 앱 테스트 실행
            continue

if __name__ == '__main__':
    main()
