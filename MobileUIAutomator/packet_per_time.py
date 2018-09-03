import csv
from operator import itemgetter

targets = ['coupang.csv',
           'ebay.csv',
           'amazon.csv',
           'auction.csv',
           'gmarket.csv']


def main():
    for target in targets:
        print(target)
        with open(target, 'r') as f:
            reader = csv.DictReader(f)
            result_dict = dict()
            pivot = None
            for row in reader:
                if row['Protocol'] == 'ICMP' and row['Destination'] == 'localhost':
                    pivot = int(row['Time'])
                if pivot is not None:
                    result_dict[pivot] = [result_dict.get(pivot, [0, 0])[0] + 1,
                                          result_dict.get(pivot, [0, 0])[1] + int(row['Length'])]
            result_list = list()
            for key in result_dict.keys():
                result_list.append((key, result_dict[key][0], result_dict[key][1]))
            result_list = sorted(result_list, key=itemgetter(0))
            for result in result_list:
                print(result)


if __name__ == '__main__':
    main()