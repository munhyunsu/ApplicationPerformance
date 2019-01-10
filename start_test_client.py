import sys

ARGS = None


def main():
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip',
                        type=str,
                        required=True,
                        help='test server ip address')

    parser.add_argument('-p', '--port',
                        type=int,
                        required=True,
                        help='test server port number')
    ARGS = parser.parse_args()

    main()

