import os
import csv

from pcap_to_csv import PcapToCSV


def get_files(path, ext='', recursive=False):
    path_list = [path]

    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        yield entry.path
                    else:
                        if recursive:
                            path_list.append(entry.path)


def get_nintynine(csv_path):
    volume = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                volume = volume + int(row.get('ip.len', 0))
            except ValueError:
                pass

    return volume * 0.99


def get_nintynine_time(csv_path, thresh):
    volume = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                volume = volume + int(row.get('ip.len', 0))
            except ValueError:
                pass
            if volume > thresh:
                return row.get('frame.time_relative')


def main():
    for file_path in get_files('pcaps', ext='pcap'):
        pcap_reader = PcapToCSV(file_path)
        csv_path = pcap_reader.get_csv_path()
        print(file_path, get_nintynine_time(csv_path, get_nintynine(csv_path)))


if __name__ == '__main__':
    main()
