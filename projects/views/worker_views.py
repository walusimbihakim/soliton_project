from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from projects.decorators.auth_decorators import supervisor_required
from projects.forms.worker_forms import WorkerForm
from projects.selectors.workers import get_all_workers, get_worker, get_all_workers_registered_by


@supervisor_required
def manage_workers_page(request):
    workers = get_all_workers_registered_by(request.user)
    form = WorkerForm()
    if request.method == "POST":
        form = WorkerForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.registered_by_user = request.user
            worker.save()
            messages.success(request, "Successfully added a worker")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_workers_page))
    context = {
        "workers_page": "active",
        "manage_workers": "active",
        "workers": workers,
        'form': form,
    }
    return render(request, "worker/manage_workers.html", context)


@supervisor_required
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
        "workers_page": "active",
        "manage_workers": "active",
        "form": form,
    }
    return render(request, "worker/edit_worker.html", context)


@supervisor_required
def delete_worker(request, id):
    worker = get_worker(id)
    worker.delete()
    messages.success(request, "Successfully deleted a worker")
    return HttpResponseRedirect(reverse(manage_workers_page))
