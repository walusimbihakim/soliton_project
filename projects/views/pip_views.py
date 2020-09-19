from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from projects.forms.pip_forms import PIPForm
from projects.selector.pip_selectors import get_pips, get_pip

def pip_page_view(request, scope_id):
    pip_form = PIPForm()

    if request.method=="POST":
        pip_form=PIPForm(request.POST, request.FILES)

        if pip_form.is_valid():
            pip_form.save()

            messages.success(request, 'PIP record Saved Successfully')
        
        else:
            messages.warning(request, 'One or more Inputs not in correct format, check and try again')

    pips = get_pips(scope_id)
    scope = get_scope(scope_id)

    context = {
        "pips": pips,
        "pip_form": pip_form,
        "scope": scope
    }

    return render(request, "manage_pips.html", context)

def edit_pip_view(request, pip_id):
    pip = get_pip(pip_id)

    pip_form = PIPForm(intance=pip)

    if request.method=="POST":
        pip_form = PIPForm(request.POST, request.FILES)

        if pip_form.is_valid():
            pip_form.save()

            messages.success(request, 'PIP Record changes saved Successfully')

            return HttpResponseRedirect(reverse(pip_page_view, args=[pip.scope.id]))

        else:
            messages.warning(request, 'One or more Inputs not in correct format, check and try again')
    
    pips = get_pips(pip.scope.id)
    # scope = get_scope(scope_id)

    context = {
        "pips": pips,
        "pip_form": pip_form,
    }

    return render(request, "edit_pip.html", context)