from django.http import HttpResponse


def view_main(request):
    return HttpResponse('you are here!')