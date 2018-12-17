import csv

from sklearn.cluster import KMeans

PATH = '/home/harny/Github/ApplicationPerformance/PerformanceScore/181211-a5-3g-init-result.csv'
N_CLUSTERS = 13

def main():
    apps = list()
    data = list()
    result = dict()
    for index in range(0, N_CLUSTERS):
        result[index] = list()
    with open(PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            apps.append(row[0])
            data.append(row[2:6])
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0).fit(data)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    count = 0
    for predict_value in labels:
        result[predict_value].append(apps[count])
        count = count + 1
    print('FP, LL, CS, RT')
    for index in range(0, N_CLUSTERS):
        print('Center: {0}'.format(centers[index]))
        print(result[index])


def main2():
    apps = list()
    data = list()
    result = dict()
    for N_CLUSTERS in range(2, 50):
        for index in range(0, N_CLUSTERS):
            result[index] = list()
        with open(PATH, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                apps.append(row[0])
                data.append(row[1:6])
        kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0).fit(data)
        print(N_CLUSTERS, kmeans.inertia_)


if __name__ == '__main__':
    main()
    # main2()
