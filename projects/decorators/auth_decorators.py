from django.http import HttpResponseRedirect
from django.urls import reverse


def super_admin_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('super_admin_required_page'))

    return wrapper
