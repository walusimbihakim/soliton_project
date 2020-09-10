from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse

from projects.forms.worker_forms import WorkerForm
from projects.selectors.workers import get_all_workers, get_worker


def manage_workers_page(request):
    workers = get_all_workers()
    form = WorkerForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a worker")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_workers_page))
    context = {
        "wagebill": "active",
        "manage_workers": "active",
        "workers": workers,
        'form': form,
    }
    return render(request, "wagebill/manage_workers.html", context)


def edit_worker_page(request, id):
    worker = get_worker(id)
    form = WorkerForm(instance=worker)
    if request.method == "POST":
        form = WorkerForm(request.POST, request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a worker")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_workers_page))
    context = {
        "wagebill": "active",
        "manage_workers": "active",
        "form": form,
    }
    return render(request, "wagebill/edit_worker.html", context)


def delete_worker(request, id):
    worker = get_worker(id)
    worker.delete()
    messages.success(request, "Successfully deleted a worker")
    return HttpResponseRedirect(reverse(manage_workers_page))
