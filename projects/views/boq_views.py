from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from projects.forms.material_boq_form import MaterialBOQForm
from projects.forms.service_boq_form import ServiceBOQForm
from projects.selectors.boq import get_boq, get_materialboqitems, get_serviceboqitems, get_material_boq_item, \
    get_service_boq_item
from projects.selectors.project_selectors import get_projects, get_project, get_surveys, get_survey
from projects.services.boq_services import create_boq_from_survey


def manage_boqs(request):
    projects = get_projects()
    context = {
        'projects': projects,
    }
    return render(request, "boq/manage_boqs.html", context)


def manage_project_boqs(request, id):
    project = get_project(id)
    surveys = get_surveys(project)
    context = {
        'surveys': surveys,
    }
    return render(request, "boq/manage_project_boqs.html", context)


def manage_boq_items(request, id):
    boq = get_boq(id)
    materialboqitems = get_materialboqitems(boq)
    materialboqform = MaterialBOQForm()
    serviceboqitems = get_serviceboqitems(boq)
    serviceboqform = ServiceBOQForm()

    context = {
        'materialboqitems': materialboqitems,
        'materialboqform': materialboqform,
        'serviceboqitems': serviceboqitems,
        'serviceboqform': serviceboqform,
        "boq": boq
    }
    return render(request, "boq/manage_boq_items.html", context)


def add_materialboq(request, id):
    boq = get_boq(id)
    form = MaterialBOQForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            materialboq = form.save(commit=False)
            materialboq.boq = boq
            try:
                materialboq.save()
            except IntegrityError:
                messages.error(request, "Material BOQ Item already available. You can delete or edit it")
                return HttpResponseRedirect(reverse(manage_boq_items, args=[id]))
            messages.success(request, "Successfully added a material BOQ item")
        else:
            messages.error(request, "Integrity problems while saving material BOQ item")

    return HttpResponseRedirect(reverse(manage_boq_items, args=[id]))


def edit_materialboq(request, id):
    material_boq_item = get_material_boq_item(id)
    materialboqform = MaterialBOQForm(instance=material_boq_item)
    if request.method == "POST":
        materialboqform = MaterialBOQForm(request.POST, instance=material_boq_item)
        if materialboqform.is_valid():
            materialboqform.save()
            messages.success(request, "Successfully edited a material BOQ Item")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_boq_items, args=[material_boq_item.boq.id]))
    context = {
        "material_boq_item": material_boq_item,
        "materialboqform": materialboqform,
    }
    return render(request, "boq/edit_material.html", context)


def delete_materialboq(request, id):
    material_boq_item = get_material_boq_item(id)
    material_boq_item.delete()
    messages.success(request, "Successfully deleted a material BOQ Itemr")
    return HttpResponseRedirect(reverse(manage_boq_items, args=[material_boq_item.boq.id]))


def add_serviceboq(request, id):
    boq = get_boq(id)
    form = ServiceBOQForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            serviceboq = form.save(commit=False)
            serviceboq.boq = boq
            try:
                serviceboq.save()
            except IntegrityError:
                messages.error(request, "Service BOQ Item already available. You can delete or edit it")
                return HttpResponseRedirect(reverse(manage_boq_items, args=[id]))
            messages.success(request, "Successfully added a service BOQ item")
        else:
            messages.error(request, "Integrity problems while saving BOQ item")
    return HttpResponseRedirect(reverse(manage_boq_items, args=[id]))


def edit_serviceboq(request, id):
    service_boq_item = get_service_boq_item(id)
    serviceboqform = ServiceBOQForm(instance=service_boq_item)
    if request.method == "POST":
        serviceboqform = ServiceBOQForm(request.POST, instance=service_boq_item)
        if serviceboqform.is_valid():
            serviceboqform.save()
            messages.success(request, "Successfully edited a service BOQ Item")
        else:
            messages.error(request, "Integrity problems while saving BOQ item")
        return HttpResponseRedirect(reverse(manage_boq_items, args=[service_boq_item.boq.id]))

    context = {
        "service_boq_item": service_boq_item,
        "serviceboqform": serviceboqform,
    }
    return render(request, "boq/edit_service.html", context)


def delete_serviceboq(request, id):
    service_boq_item = get_service_boq_item(id)
    service_boq_item.delete()
    messages.success(request, "Successfully deleted a service BOQ Item")
    return HttpResponseRedirect(reverse(manage_boq_items, args=[service_boq_item.boq.id]))


def create_boq(request, survey_id):
    survey = get_survey(survey_id)
    boq = create_boq_from_survey(survey)
    return HttpResponseRedirect(reverse(manage_boq_items, args=[boq.id]))
