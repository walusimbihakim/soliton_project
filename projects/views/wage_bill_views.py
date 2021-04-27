import csv

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import datetime

import projects.forms.wage_bill_forms as wage_bill_forms
import projects.selectors.wage_bill_selectors as wage_bill_selectors
from projects.decorators.auth_decorators import finance_office_required
from projects.selectors.workers import get_worker
from projects.services.wage_bill_services import set_current_wage_bill_status_to_done, send_wage_created_email_service


@finance_office_required
def manage_wage_bill(request):
    wage_bill_form = wage_bill_forms.WageBillForm()
    if request.method == "POST":
        wage_bill_form = wage_bill_forms.WageBillForm(request.POST, request.FILES)
        if wage_bill_form.is_valid():
            set_current_wage_bill_status_to_done()
            wage_bill_form.save()
            send_wage_created_email_service()
            messages.success(request, "Wage Bill Record Saved Successfully")
        else:
            messages.warning(request, "Something went wrong, check your Input and try again")
    wagebills = wage_bill_selectors.get_wage_bills()
    context = {
        "wage_bill_page": "active",
        "wagebills": wagebills,
        "wage_bill_form": wage_bill_form
    }
    return render(request, "wage_bill/manage_wage_bill.html", context)


@finance_office_required
def edit_wage_bill(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    wage_bill_form = wage_bill_forms.WageBillForm(instance=wage_bill)

    if request.method == "POST":
        wage_bill_form = wage_bill_forms.WageBillForm(request.POST, request.FILES, instance=wage_bill)

        if wage_bill_form.is_valid():
            wage_bill_form.save()

            messages.success(request, "Changes Saved Successfully")

        else:
            messages.error(request, "Something went wrong, check your Input and try again")
        return HttpResponseRedirect(reverse(manage_wage_bill))
    context = {
        "wage_bill_page": "active",
        "manage_wage_bill": "active",
        "wage_bill_form": wage_bill_form,
    }
    return render(request, "wage_bill/edit_wage_bill.html", context)


@finance_office_required
def delete_wage_bill(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)

    wage_bill.delete()

    messages.success(request, "Wage bill Deleted Successfully")
    return HttpResponseRedirect(reverse(manage_wage_bill))


def get_end_date(request):
    if request.method == "GET":
        date_format = "%Y-%m-%d"

        # Capturing values from the request
        start_date = request.GET["start_date"]

        if start_date:

            start_date = datetime.datetime.strptime(start_date, date_format)

            end_date = start_date + datetime.timedelta(days=7)

            if end_date is None:
                return JsonResponse({'success': False, 'message': 'No Date returned'})

            return JsonResponse({'success': True, 'end_date': end_date.date()})
        else:
            return JsonResponse({'success': False, 'message': "Start Date and/or Number of days Not Specified"})


@finance_office_required
def current_consolidated_wage_bill(request):
    wage_bill = wage_bill_selectors.get_current_wage_bill()
    aggregated_wages = wage_bill_selectors.get_aggregated_wage_bill(wage_bill)
    context = {
        "wage_bill_page": "active",
        "wage_bill": wage_bill,
        "aggregated_wages": aggregated_wages,
    }
    return render(request, "wage_bill/consolidated_wage_bill.html", context)


@finance_office_required
def consolidated_wage_bill(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id=wage_bill_id)
    aggregated_wages = wage_bill_selectors.get_aggregated_wage_bill(wage_bill)
    context = {
        "wage_bill_page": "active",
        "wage_bill": wage_bill,
        "aggregated_wages": aggregated_wages,
    }
    return render(request, "wage_bill/consolidated_wage_bill.html", context)


def consolidated_wage_bill_csv(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id=wage_bill_id)
    aggregated_wages = wage_bill_selectors.get_aggregated_wage_bill(wage_bill)
    response = HttpResponse(content_type='text/csv')
    # Name the csv file
    filename = f"Wage Bill {wage_bill}.csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=',')
    # Writing the first row of the csv
    writer.writerow(
        ['No', 'Worker', 'Telephone', 'Amount', 'Charge',
         'Total'])
    # Writing other rows
    for index, wage in enumerate(aggregated_wages):
        worker_id = wage['worker']
        payment = int(wage['payment'])
        worker = get_worker(id=worker_id)
        charge = wage_bill_selectors.get_airtel_money_withdraw_charge(payment)
        total = payment + charge
        number = index + 1
        writer.writerow(
            [number, worker, worker.mobile_money_number, payment, charge, total])
    return response
