from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from projects.models import UnitOfMeasure
from projects.forms.project_settings_forms import UnitOfMeasureForm
from projects.selectors.project_settings_selectors import get_measures

def unit_of_measure_view(request):
    unit_form = UnitOfMeasureForm()

    if request.method == "POST":
        unit_form = UnitOfMeasureForm(request.POST)

        if unit_form.is_valid():
            unit_form.save()

            messages.success(request, 'Unit Measure added Successfully')

    units_of_measures = get_measures()

    context = {
        "unit_form": unit_form,
        "units": units_of_measures
    }

    return render(request, "uom/uom.html", context)
