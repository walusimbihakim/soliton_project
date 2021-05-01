import csv

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from project_manager.settings import BASE_DIR
from projects.decorators.auth_decorators import supervisor_required, project_manager_required
from projects.forms.worker_forms import WorkerForm
from projects.procedures import render_to_pdf
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


@project_manager_required
def view_all_workers_page(request):
    workers = get_all_workers()
    context = {
        "workers_page": "active",
        "view_all_workers": "active",
        "workers": workers,
    }
    return render(request, "worker/view_all_workers.html", context)


def all_workers_csv(request):
    workers = get_all_workers()
    response = HttpResponse(content_type='text/csv')
    # Name the csv file
    filename = f"Workers.csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=',')
    # Writing the first row of the csv
    writer.writerow(
        ['No', 'Name', 'Type', 'Business Unit', 'National ID', 'Joined Date', 'Gender',
         'Mobile Money Number', 'Address', 'Next of kin', 'Supervisor', 'Registered By'])
    # Writing other rows
    for worker in workers:
        writer.writerow(
            [worker.id, worker.name, worker.type, worker.business_unit, worker.national_ID_NIN,
             worker.joining_date, worker.gender, worker.mobile_money_number, worker.address,
             worker.next_of_kin, worker.registered_by_user, worker.registered_by_user])
    return response


def all_workers_pdf(request):
    workers = get_all_workers()
    context = {
        "base_dir": BASE_DIR,
        "view_all_workers": "active",
        "workers": workers,
    }
    pdf = render_to_pdf('pdfs/all_workers.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


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
