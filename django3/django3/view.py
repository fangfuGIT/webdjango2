from django.http import HttpResponse,HttpRequest


def test(request):
    return HttpResponse('test')