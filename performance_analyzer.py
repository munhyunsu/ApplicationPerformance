import sys

from util.path import std_path

ARGS = None

def main():
    print(ARGS)


if __name__ == '__main__':
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-iv', '--input-video', type=str, required=True,
                        help='input video directory path')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='output directory path')

    ARGS = parser.parse_args()

    # Preprocessing arguments
    if 'input_video' in ARGS:
        ARGS.input_video = std_path(ARGS.input_video)
    if 'output' in ARGS:
        ARGS.output = std_path(ARGS.output)

    main()
    
