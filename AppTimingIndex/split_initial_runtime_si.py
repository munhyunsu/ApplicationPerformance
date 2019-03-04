import csv
import statistics


def main(argv):
    inits = dict()
    runtime = dict()
    for path in argv[1:-3]:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if eval(row[1])[0] == 0:
                    init = inits.get(row[0], list())
                    init.append(float(row[2]))
                    inits[row[0]] = init
                elif float(row[2]) >= 100:
                    runs = runtime.get(row[0], list())
                    runs.append(float(row[2]))
                    runtime[row[0]] = runs
    with open(argv[-3], 'w') as f:
        writer = csv.writer(f)
        for key in inits.keys():
            for entry in inits[key]:
                writer.writerow((key, entry))
    with open(argv[-2], 'w') as f:
        writer = csv.writer(f)
        for key in runtime.keys():
            for entry in runtime[key]:
                writer.writerow((key, entry))
    with open(argv[-1], 'w') as f:
        writer = csv.writer(f)
        for key in runtime.keys():
            writer.writerow((key, statistics.mean(inits[key])*0.7 + statistics.mean(runtime[key])*0.3))


if __name__ == '__main__':
    import sys
    print(sys.argv)
    sys.exit(main(sys.argv))
