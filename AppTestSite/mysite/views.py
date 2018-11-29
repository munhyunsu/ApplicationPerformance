from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from speed.models import AppInformation, SpeedInformation

import csv
from operator import itemgetter


def index(request):
    if request.method == 'GET':
        apps = AppInformation.objects.all().order_by('app_title')
        return render(request, 'index.html', {'apps': apps})


def result(request):
    if request.method == 'GET':
        package_name = request.GET.get('package')
        app_title = AppInformation.objects.get(package_name=package_name).app_title
        exps = SpeedInformation.objects.filter(package_name=package_name).order_by('-exp_date', 'scene_num')
        return render(request, 'result.html', {'app_title': app_title,
                                               'exps': exps})


def new(request):
    if request.method == 'GET':
        pkgname = None
    elif request.method == 'POST':
        pkgname = request.POST.get('pkgname')
    return render(request, 'new.html', {'pkgname': pkgname})
