from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def result(request):
    template = loader.get_template('result.html')
    return HttpResponse(template.render())


def advice(request):
    template = loader.get_template('advice.html')
    return HttpResponse(template.render())
