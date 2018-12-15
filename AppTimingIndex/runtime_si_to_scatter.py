import csv
import statistics

#def main(argv):
#    with open(argv[1], 'r') as f:
#        reader = csv.reader(f)
#        app = dict()
#        runtime = list()
#        count = 1
#        rank = list()
#        for row in reader:
#            if row[0] not in app.keys():
#                count = count + 1
#                if row[2] not in rank:
#                    rank.append(row[2])
#                    app[row[0]] = (row[2], count)
#                else:
#                    rank.append(str(float(row[2])+0.0001))
#                    app[row[0]] = (str(float(row[2])+0.0001), count)
#            elif float(row[2]) >= 100:
#                runtime.append((app[row[0]][0], row[2]))
#    with open(argv[2], 'w') as f:
#        rank.sort()
#        writer = csv.writer(f)
#        for entry in runtime:
#            writer.writerow((rank.index(entry[0])+1, entry[0], entry[1]))


def main(argv):
    app = dict()
    runtime = dict()
    for path in argv[1:-1]:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if eval(row[1])[0] == 0:
                    if row[0] not in app.keys():
                        app[row[0]] = row[2]
                    elif app[row[0]] > row[2]:
                        app[row[0]] = row[2]
                elif float(row[2]) >= 100:
                    runs = runtime.get(row[0], list())
                    runs.append(float(row[2]))
                    runtime[row[0]] = runs
    with open(argv[-1], 'w') as f:
        writer = csv.writer(f)
        for key in runtime.keys():
            writer.writerow((key, app[key][0], statistics.mean(runtime[key])))


if __name__ == '__main__':
    import sys
    print(sys.argv)
    sys.exit(main(sys.argv))
