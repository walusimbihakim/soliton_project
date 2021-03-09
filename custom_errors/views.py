from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def error_500(request):
    data = {}
    response = render(request, "custom_errors/500.html", data)
    return HttpResponseServerError(response)


def error_404(request, exception):
    data = {}
    response = render(request, "custom_errors/404.html", data)
    return HttpResponseNotFound(HttpResponse=response)


def error_403(request, exception):
    data = {}
    response = render(request, "custom_errors/403.html", data)
    return HttpResponseForbidden(response)

