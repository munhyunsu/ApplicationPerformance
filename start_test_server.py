import sys

from src.client_ui import ClientUI


ARGS = None


def main():
    ui = ClientUI()
    if ARGS.package is None:
        ARGS.package = ui.query_package()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package',
                        help='test package name')

    ARGS = parser.parse_args()

    main()

