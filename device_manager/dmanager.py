import sys


ARGS = None

def main():
    print(ARGS)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', type=str,
                        help='device model for creation')
    parser.parse_args()

    main()

