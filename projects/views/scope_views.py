from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from projects.forms.execution_scope_form import ExecutionScopeForm
from projects.selectors.scopes import get_all_scopes


def manage_scopes_page(request):
    scopes = get_all_scopes()
    form = ExecutionScopeForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a scope")
        else:
            messages.error(request, "Integrity problems while saving scope")
        return HttpResponseRedirect(reverse(manage_scopes_page))
    context = {
        "manage_scopes": "active",
        "scopes": scopes,
        'form': form,
    }
    return render(request, "scope/manage_survey_scopes.html", context)
