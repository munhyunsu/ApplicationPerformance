import csv
import statistics
from operator import itemgetter


def main(argv):
    print(argv)
    runtime = dict()
    app = dict()
    max_len = -1
    for path in argv[1:-1]:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            print(path)
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
                    if len(runs) > max_len:
                        max_len = len(runs)
    with open(argv[-1], 'w') as f:
        app_rank = list()
        for key in runtime.keys():
            app_rank.append((key, app[key]))
        app_rank.sort(key=itemgetter(1))
        writer = csv.writer(f)
        for entry in app_rank:
            key = entry[0]
        #for key in runtime.keys():
            try:
                runs = runtime[key]
                print([key] + runs)
                writer.writerow([key] + runs + ['']*(max_len-len(runs)))
            except:
                continue


if __name__ == '__main__':
    import sys
    main(sys.argv)
    
