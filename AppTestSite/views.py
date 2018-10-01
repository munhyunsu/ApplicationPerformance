from django.http import HttpResponse
from django.template import loader

import csv
from operator import itemgetter


def index(request):
    template = loader.get_template('index.html')
    data_list = list()
    with open('data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['si'] = int(float(row['si']))
            data_list.append(row)
    data_list.sort(key=itemgetter('si'))
    return HttpResponse(template.render({'result': data_list}))


def result(request):
    template = loader.get_template('result.html')
    package = request.GET.get('package')

    data_list = list()
    with open('data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for header in ['si', 'tcp', 'http', 'https', 'rexmit', 'layout', 'lastlayout', 'ads', 'image']:
                row[header] = int(float(row[header]))
            for header in ['rtt', 'idletime', 'xmittime']:
                row[header] = float(row[header])
            data_list.append(row)
            if package == row['packagename']:
                target = row
    target_dict = dict()
    for header in ['si', 'rtt', 'idletime', 'xmittime', 'tcp', 'http', 'https', 'rexmit', 'layout', 'lastlayout', 'ads', 'image']:
        data_list.sort(key=itemgetter(header))
        target_dict[header] = float((data_list.index(target)+1)/len(data_list))

    return HttpResponse(template.render({'package': package, 'result': target, 'rank': target_dict}))


def advice(request):
    template = loader.get_template('advice.html')
    return HttpResponse(template.render())
