import os
import sys
import configparser
import logging

FLAGS = None


def do_analysis(path):
    logging.debug(f'Start analyze {path}')


def main():
    config = configparser.ConfigParser()
    config.read(FLAGS.config)

    do_analysis(os.path.abspath(os.path.expanduser(config['Data']['Path'])))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str,
                        help='Configuration file path',
                        default='config.ini')
    parser.add_argument('-v', '--verbose', action='count')

    FLAGS, _ = parser.parse_known_args()

    # Convert relative path to absolute path
    FLAGS.config = os.path.abspath(os.path.expanduser(FLAGS.config))

    # Set logging level
    dlvl = logging.INFO
    if FLAGS.verbose is not None:
        if FLAGS.verbose > 0:
            dlvl = logging.DEBUG
    logging.basicConfig(stream=sys.stdout, level=dlvl)

    main()

