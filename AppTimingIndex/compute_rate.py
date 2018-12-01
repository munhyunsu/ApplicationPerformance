import csv


def main():
    result = dict()
    with open('amazon_timing.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample = dict()
            sample['dns'] = float(row.get('domainLookupEnd', 0.0)) - float(row.get('domainLookupStart', 0.0))
            sample['connect'] = float(row.get('secureConnectionStart', 0.0)) - float(row.get('connectStart', 0.0))
            sample['secure'] = float(row.get('requestStart', 0.0)) - float(row.get('secureConnectionStart', 0.0))
            sample['request'] = float(row.get('responseStart', 0.0)) - float(row.get('requestStart', 0.0))
            sample['response'] = float(row.get('responseEnd', 0.0)) - float(row.get('responseStart', 0.0))
            for key in sample.keys():
                if sample[key] > 0:
                    result[key] = result.get(key, 0) + sample[key]
    total = 0
    for key in result:
        total = total + result[key]

    print('ratio')
    for key in result.keys():
        print(key, result[key]/total)


if __name__ == '__main__':
    main()
