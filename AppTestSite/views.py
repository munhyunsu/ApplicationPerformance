from django.http import HttpResponse


def index(request):
    return HttpResponse('you are in index page')


def result(request):
    return HttpResponse('You are in result page')


def advice(request):
    return HttpResponse('You are in advice page')