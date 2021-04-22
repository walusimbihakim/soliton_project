from django.http import HttpResponseRedirect
from django.urls import reverse

from projects.constants import PROJECT_MANAGER, SUPERVISOR, FINANCE_OFFICER


def super_admin_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('super_admin_required_page'))
    return wrapper


def project_manager_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.user_role == PROJECT_MANAGER or user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('project_manager_required_page'))
    return wrapper


def supervisor_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.user_role == SUPERVISOR or user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('supervisor_required_page'))
    return wrapper


def finance_office_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.user_role == FINANCE_OFFICER or user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('finance_officer_required_page'))
    return wrapper
