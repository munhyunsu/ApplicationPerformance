import sys

from util.path import std_path

ARGS = None

def main():
    xml_dir = os.path.join(ARGS.input, 'xml')
    mp4_dir = os.path.join(ARGS.input, 'mp4')


if __name__ == '__main__':
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-iv', '--input', type=str, required=True,
                        help='input video directory path')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='output directory path')

    ARGS = parser.parse_args()

    # Preprocessing arguments
    if 'input' in ARGS:
        ARGS.input = std_path(ARGS.input)
    if 'output' in ARGS:
        ARGS.output = std_path(ARGS.output)

    main()
    
