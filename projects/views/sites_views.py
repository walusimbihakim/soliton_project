from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from projects.forms.site_forms import SiteForm
from projects.selectors.sites_selectors import *
from projects.selectors.project_selectors import *


def sites_page_view(request, project_id):
    site_form = SiteForm(
        request.POST,
        request.FILES,
        initial={
            'project': project_id
        }
    )

    if request.method == "POST":
        if site_form.is_valid():
            site_form.save()

    sites = get_sites(project_id)
    project = get_project(project_id)

    context = {
        "project": project,
        "sites": sites,
        "site_form": site_form
    }

    return render(request, "manage_sites.html", context)


def site_details_view(request, project_id, site_id):
    site = get_site(site_id)

    context = {
        "site": site,
    }
    return render(request, "site_details.html", context)
