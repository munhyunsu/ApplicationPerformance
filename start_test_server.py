import os
import sys

from src.client_ui import ClientUI
#from src.apk_downloader import APKDownloader

ARGS = None


def main():
    ui = ClientUI()
    if ARGS.driver is None:
        ARGS.driver = ui.query_args('driver')
    ARGS.driver = os.path.abspath(os.path.expanduser(ARGS.driver))
    if ARGS.package is None:
        ARGS.package = ui.query_args('package')

    print('ARGS', ARGS)
#    downloader = APKDownloader(ARGS.driver)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package',
                        type=str,
                        help='test package name')
    parser.add_argument('-d', '--driver',
                        type=str,
                        default='./webdriver/chromedriver',
                        help='web driver path')

    ARGS = parser.parse_args()

    main()

