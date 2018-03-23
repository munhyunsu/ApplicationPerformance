import subprocess
import time
import configparser
import os
import datetime
import logging
import random
import re
from xml.etree.ElementTree import parse

class DeviceController:

    def __init__(self):
        # 설정파일 읽어와서 환경변수 설정
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")

            self.adb_location = config.get("device_controller",\
                "adb_location")
            self.apk_directory = config.get("device_controller",\
                "apk_directory")
            self.tcpdump_directory = config.get("device_controller",\
                "tcpdump_directory")
            self.pcap_save_directory = config.get("device_controller",\
                "pcap_save_directory")
            self.save_directory = config.get("device_controller",\
                "save_directory")
            self.save_directory = save_directory + \
                datetime.datetime.now().strftime('%y%m%d') + '/'

            os.makedirs(save_directory)
        except FileExistsError as e: # 파일이 이미 존재한다면 넘어간다.
            pass
        except Exception as e:
            raise e


    def reboot(self):
        """
        단말기 재부팅시키기.
        adb shell reboot가 안정적인 재부팅 명령어인지는 확인해야한다.
        adb shell reboot 명령어 실행 후, 10초간격으로 adb연결된 device가
        있는지 확인(재부팅 완료되었는지 확인) 연결을 확인한 후
        10초 후 함수 종료
        output- 재연결 확인이 완료되면 True반환
        """

        # 리부팅 명령어 실행
        command = adb_location + 'adb shell reboot'
        try:
            proc_reboot = subprocess.Popen(command, shell=True)
            time.sleep(10)
        except Exception as e:
            logging.error(' adb shell reboot error')
            raise e


        # 단말기가 재부팅 완료 후 연결이 정상적으로 되어있는지 확인
        # adb device의 결과값을 확인
        command = adb_location + 'adb devices'
        while True:
            try:
                proc_check_on = subprocess.Popen(command, shell=True)
                output = str(proc_check_on.stdout.read())
                devices = output.split("\\n")
                # 연결된 단말기가 1개 있으면 len이 4
                if len(devices) == 4:
                    time.sleep(10)
                    logging.info('단말기 재연결 확인 완료')
                    break
                else: # 연결된 단말기가 없다면 3으로 나온다.
                    time.sleep(10)
            except Exception as e:
                time.sleep(10)
                continue

        return True

    def run_test(self, pkg_name):
        """
        APK파일 이름을 받아서 테스트 진행
        설치 -> 실행 -> 테스트 -> 종료 및 삭제 -> pcap,mp4 파일 추출
        install 에서 에러났을경우에만 재부팅 하도록 한다.
        (단말기 공간이 모두 찼을경우 존재하므로)

        pkg_name : 패키지이름(APK파일 이름)
        """

        # 데이터를 수집할 디렉토리가 없다면 미리 생성
        # 이미 디렉토리가 존재한다면 pass
        try:
            os.makedirs(save_directory + 'pcap')
            os.makedirs(save_directory + 'record')
        except FileExistsError as e:
            print(e)
            pass
        except Exception as e:
            raise e
        try:
            os.makedirs(save_directory + 'xml/' + pkg_name)
        except Exception as e:
            return
        try:
            pcap_name = pkg_name + '.pcap'
            apk_name = pkg_name + '.apk'
            mp4_name = pkg_name + '.mp4'

            # apk파일 설치
            command = adb_location + "adb install " + apk_directory + apk_name
            subprocess.check_call(command, shell=True)

            # tcpdump 실행(Popen으로 Background로 실행)
            command = adb_location + "adb shell su -c " + tcpdump_directory + "tcpdump -i wlan0 -w " +\
                pcap_save_directory + pcap_name + " -s 0"
            proc_tcpdump = subprocess.Popen(command, shell=True)

            # 화면 녹화(Popen으로 Background로 실행) 
            command = adb_location + "adb shell screenrecord " + pcap_save_directory + mp4_name
            proc_record = subprocess.Popen(command, shell=True)

            # 화면 녹화 시작시간 파악
            initial_time = datetime.datetime.now()

            # monkey로 이벤트를 발생시키면서 uiautomator로 관찰
            event_index = 0
            count = 0
            session = []

            # 첫 이벤트는 앱실행도 같이 시켜야 하기 때문에 monkey로 이벤트 발생
            command = adb_location + "adb shell monkey -p " + pkg_name + " --pct-touch 100 3"
            subprocess.check_call(command, shell=True)
            time.sleep(5)

            # 총 5개의 이벤트 발생
            num_of_event = 5

            while(event_index < num_of_event):
                prev_count = -1
                total_count = 0
                while(True):
                    # uiautomator를 batch job으로 무한반복시키면서 node 개수 파악 
                    snap_time = datetime.datetime.now() - initial_time
                    command = adb_location + "adb shell su -c uiautomator dump /sdcard/xml/" +\
                        str(int(snap_time.total_seconds())) + ".xml"
                    uiautomator_output = subprocess.check_output(command, shell=True)
                    uiautomator_output = uiautomator_output.decode('utf-8')
                    if "ERROR" in uiautomator_output:
                        print("uiautomator error app")
                        break

                    # 서버에서 앱 실행전에 uiautomator가 동작하면 파일이 생성되지 않는 문제가 존재
                    try:
                        command = adb_location + "adb pull /sdcard/xml/" + str(int(snap_time.total_seconds())) + ".xml " +\
                            save_directory + 'xml/' + pkg_name + '/'
                        subprocess.check_call(command, shell=True, stdout=None)
                    except Exception as e:
                        continue

                    # xml파일 파싱하여 node 개수 파악
                    tree = parse(save_directory + 'xml/' + pkg_name + '/' + str(int(snap_time.total_seconds())) + ".xml")
                    root = tree.getroot()
                    iterator =  root.iter()

                    # 현재화면에서 터치할 수 있는 객체 가져오는 리스트
                    clickable_list = []
                    node_count = 0
                    for item in iterator:
                        node_count = node_count + 1

                        if(item.get('clickable') == 'true'):
                            clickable_list.append(item)
                    print('node count : ' + str(node_count))

                    # 이전 xml파일과 노드개수가 불일치하면 아직 렌더링중이므로 노드개수 갱신
                    if(prev_count != node_count):
                        prev_count = node_count
                        count = 0
                    else:
                        count = count + 1

                    # 노드개수가 5개의 xml파일동안 동일하면 렌더링 완료
                    if((count == 3) | (total_count >= 20)):
                        print('event detected')
                        snap_time = datetime.datetime.now() - initial_time
                        print('snap time : ' + str(int(snap_time.total_seconds())) + '\n\n')
                        session.append(str(int(snap_time.total_seconds())))

                        # 터치할 수 있는 객체중 하나 랜덤으로 선택하여 해당 좌표로 입력이벤트 발생시킴
                        # 터치할 수 있는 객체중에 레이아웃도 있는데 그때는 0,0이 나옴. 그것은 자동필터링
                        # TODO: 화면 안에 터치할 수 잇는 버튼이 없을 가능성이 있나 ?
                        if(len(clickable_list) !=0):
                            while(True):
                                bounds = random.choice(clickable_list).get('bounds')
                                bounds = re.split('\[|\]|,',bounds)
                                bounds = list(filter(None, bounds))
                                x = int((int(bounds[0]) + int(bounds[2]))/2)
                                y = int((int(bounds[1]) + int(bounds[3]))/2)

                                if(x!=0 and y!=0):
                                    break
                            if (event_index  != num_of_event):
                                print('x : ' + str(x) + " y : " + str(y))
                                command = adb_location + "adb shell input tap " + str(x) + " " + str(y)
                                subprocess.check_call(command, shell=True, stdout=None)
                        # 현재 화면에서 터치할 수 있는 개체가 없는경우에는 monkey로 랜덤 좌표 이벤트 발생
                        else:
                            command = adb_location + "adb shell monkey -p " + pkg_name + " --pct-touch 100 3"
                            subprocess.check_call(command, shell=True, stdout=None)
                        total_count = 0
                        break
                    total_count += 1


                event_index = event_index + 1


            # test를 마치고 csv로 저장
            file_session = open(save_directory + "/speed.csv", "a")
            file_session.write(pkg_name + "," + ','.join(str(a) for a in session) + "\n")
            file_session.close()

            # 화면녹화 프로세스 종료
            # python subprocess kill로 죽지 않음
            # adb 를 통해 프로세스번호 확인 후 kill시키기
            if(proc_record.poll() is None):
                command = adb_location + "adb shell ps |grep screenrecord"
                proc_kill = subprocess.check_output(command, shell=True)
                proc_kill = proc_kill.decode('utf-8')
                proc_kill = list(filter(None, proc_kill.split(' ')))
                record_id = proc_kill[1]
                command = adb_location + "adb shell kill -2 " + record_id
                subprocess.check_call(command, shell=True)

            # 단말기 안에 xml 파일 전부 제거
            command = adb_location + "adb shell rm /sdcard/xml/*"
            subprocess.check_call(command, shell=True)

            # tcpdump 프로세스 kill (관리자 권한으로 실행시켜서 subprocess로 안죽음)
            # 즉, 단말기 내부에서 kill명령어로 죽여야함
            command = adb_location + "adb shell ps |grep tcpdump"
            proc_kill = subprocess.check_output(command, shell=True)
            proc_kill = proc_kill.decode('utf-8')  # str형태로 캐스팅
            proc_kill = list(filter(None, proc_kill.split(' '))) # 공백문자 제거하여 리스트형태로 생성
            tcpdump_id = proc_kill[1]
            command = adb_location + "adb shell su -c kill -2 " +  tcpdump_id
            subprocess.check_call(command, shell=True)

            # 실행되어있는 앱 종료
            command = adb_location + "adb shell am force-stop " + pkg_name
            subprocess.check_call(command, shell=True)

            # pcap파일 pull
            if(proc_record.poll() is not None):
                command = adb_location + "adb pull " + pcap_save_directory + pcap_name + ' ' +\
                save_directory + 'pcap/'
                subprocess.check_call(command, shell=True)

            # mp4파일 pull
            if(proc_tcpdump.poll() is not None):
                command = adb_location + "adb pull " + pcap_save_directory + mp4_name + ' ' +\
                    save_directory + 'record/'
                subprocess.check_call(command, shell=True)


            # 단말기 내부의 mp4파일 삭제
            command = adb_location + "adb shell rm " + pcap_save_directory + '*.mp4'
            subprocess.check_call(command, shell=True)

            # 단말기 내부의 pcap파일 삭제
            command = adb_location + "adb shell rm " + pcap_save_directory + '*.pcap'
            subprocess.check_call(command, shell=True)

            # 단말기의 앱 삭제
            command = adb_location + "adb uninstall " + pkg_name
            subprocess.check_call(command, shell=True)
            logging.info(pkg_name + ' testing was finished')

        except Exception as e:
            raise e
