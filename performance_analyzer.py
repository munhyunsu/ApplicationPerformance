import sys


ARGS = None

def main():
    print(ARGS)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-iv', '--input-video', type=str, required=True,
                         help='input video directory path')

    ARGS = parser.parse_args()

    main()
    
