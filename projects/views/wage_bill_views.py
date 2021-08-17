import csv

from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import datetime

import projects.forms.wage_bill_forms as wage_bill_forms
import projects.selectors.wage_bill_selectors as wage_bill_selectors
from project_manager.settings import BASE_DIR
from projects.constants import WAGE_BILL_PAYMENT_GENERATION_CONFIRM_MESSAGE
from projects.decorators.auth_decorators import finance_office_required
from projects.procedures import render_to_pdf
from projects.selectors.workers import get_worker
from projects.selectors.user_selectors import get_user_by_id
from projects.services.wage_bill_services import remove_all_wage_bill_payments
from projects.tasks.wage_bill_payments import generate_wage_bill_task_process


@finance_office_required
def view_all_wage_bills(request):
    wagebills = wage_bill_selectors.get_wage_bills()
    paginator = Paginator(wagebills, 2)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    confirm_message = WAGE_BILL_PAYMENT_GENERATION_CONFIRM_MESSAGE
    context = {
        "wage_bill_page": "active",
        "wagebills": wagebills,
        "page_obj": page_obj,
        "confirm_message": confirm_message
    }
    return render(request, "wage_bill/view_all_wage_bills.html", context)


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
        return HttpResponseRedirect(reverse(view_all_wage_bills))
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
    return HttpResponseRedirect(reverse(view_all_wage_bills))


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
    return render(request, "wage_bill/consolidated_wage_bill_payments.html", context)


@finance_office_required
def consolidated_wage_bill(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id=wage_bill_id)
    aggregated_wages = wage_bill_selectors.get_aggregated_wage_bill(wage_bill)
    context = {
        "wage_bill_page": "active",
        "wage_bill": wage_bill,
        "aggregated_wages": aggregated_wages,
    }
    return render(request, "wage_bill/consolidated_wage_bill_payments.html", context)


@finance_office_required
def view_consolidated_wage_bill_payments(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    wage_bill_payments = wage_bill_selectors.get_all_consolidated_wage_bill_payments(wage_bill)
    paginator = Paginator(wage_bill_payments, 10)  # Show 10 payments per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "wage_bill_page": "active",
        "wage_bill": wage_bill,
        "page_obj": page_obj,
    }
    return render(request, "wage_bill/consolidated_wage_bill_payments.html", context)


@finance_office_required
def generate_consolidated_wage_bill_payments(request, wage_bill_id):
    try:
        generate_wage_bill_task_process.delay(wage_bill_id)
    except IntegrityError:
        messages.error(request, "Operation duplication")
        return HttpResponseRedirect(reverse(view_all_wage_bills))

    messages.success(request, "Generated consolidated wage bill payments from approved wages, "
                              f"complaints and deductions for wage bill week")
    return HttpResponseRedirect(reverse(view_all_wage_bills))


@finance_office_required
def reset_consolidated_wage_bill_payments(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    remove_all_wage_bill_payments(wage_bill_id)
    messages.success(request, f"Removed wage bill payments for week {wage_bill}")
    return HttpResponseRedirect(reverse(view_all_wage_bills))


def consolidated_wage_bill_payments_csv(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id=wage_bill_id)
    wage_bill_payments = wage_bill_selectors.get_all_consolidated_wage_bill_payments(wage_bill)
    response = HttpResponse(content_type='text/csv')
    # Name the csv file
    filename = f"consolidated_payments_{wage_bill}.csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=',')
    # Writing the first row of the csv
    writer.writerow(
        ['No', 'Name', 'Mobile Money Number', 'Mobile Money Name', 'Wednesday', 'Thursday', 'Friday',
         'Saturday', 'Sunday', 'Monday', 'Tuesday',
         'Total Wages', 'Total Complaints', 'Total Deductions', 'Amount', 'Charge',
         'Total Payment', 'Supervisor Name', 'Supervisor Number', 'Field Manager', 'Field Manager Number'])
    # Writing other rows
    for index, wage_bill_payment in enumerate(wage_bill_payments):
        number = index + 1
        writer.writerow(
            [number, wage_bill_payment.worker_name,
             wage_bill_payment.worker_mobile_money_number,
             wage_bill_payment.worker_mobile_money_name,
             wage_bill_payment.wednesday_total_amount,
             wage_bill_payment.thursday_total_amount,
             wage_bill_payment.friday_total_amount,
             wage_bill_payment.saturday_total_amount,
             wage_bill_payment.sunday_total_amount,
             wage_bill_payment.monday_total_amount,
             wage_bill_payment.tuesday_total_amount,
             wage_bill_payment.total_wages,
             wage_bill_payment.total_complaints,
             wage_bill_payment.total_deductions,
             wage_bill_payment.total_amount,
             wage_bill_payment.charge,
             wage_bill_payment.total_payment,
             wage_bill_payment.supervisor,
             wage_bill_payment.supervisor_number,
             wage_bill_payment.field_manager,
             wage_bill_payment.field_manager_number
             ])
    return response


def consolidated_wage_bill_pdf(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id=wage_bill_id)
    wage_bill_payments = wage_bill_selectors.get_all_consolidated_wage_bill_payments(wage_bill)
    context = {
        "wage_bill_payments": wage_bill_payments,
        "base_dir": BASE_DIR,
        "wage_bill": wage_bill
    }
    pdf = render_to_pdf('pdfs/consolidated_wage_bill_payments.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def worker_wage_bill_breakdown(request, wage_bill_id, worker_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    worker = get_worker(worker_id)
    wage_break_down = wage_bill_selectors.get_worker_wage_bill_breakdown(wage_bill, worker)
    complaint_break_down = wage_bill_selectors.get_worker_complaint_breakdown(wage_bill, worker)
    deduction_break_down = wage_bill_selectors.get_worker_deduction_breakdown(wage_bill, worker)

    context = {
        "wage_break_down": wage_break_down,
        "complaint_break_down": complaint_break_down,
        "deduction_break_down": deduction_break_down,
        "worker": worker,
    }

    return render(request, "wage_bill/worker_break_down.html", context)


def wage_bill_payment_breakdown(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    wage_break_down = wage_bill_selectors.get_wage_bill_payment_breakdown(wage_bill)
    complaint_break_down = wage_bill_selectors.get_complaint_breakdown(wage_bill)
    deduction_break_down = wage_bill_selectors.get_deduction_breakdown(wage_bill)

    context = {
        "wage_bill": wage_bill,
        "wage_break_down": wage_break_down,
        "complaint_break_down": complaint_break_down,
        "deduction_break_down": deduction_break_down,
    }

    return render(request, "wage_bill/wage_bill_break_down.html", context)


def wage_bill_manager_total(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)

    wage_bill_managers = wage_bill_selectors.get_wage_bill_managers(wage_bill)

    context = {
        'wage_bill': wage_bill,
        'wage_bill_managers': wage_bill_managers,
    }

    return render(request, "wage_bill/wage_bill_managers_total.html", context)


def wage_bill_supervisor_total(request, wage_bill_id, manager):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)

    supervisor_wage_totals = wage_bill_selectors.get_supervisor_wage_bill_total(wage_bill, manager)

    context = {
        'wage_bill': wage_bill,
        'supervisor_wage_totals': supervisor_wage_totals,
    }

    return render(request, "wage_bill/wage_bill_supervisors_total.html", context)


def wage_bill_manager_payment_breakdown(request, wage_bill_id, manager):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)

    manager_wage_sheets = wage_bill_selectors.get_manager_wage_bill_wage_sheets(wage_bill, manager)

    manager_total = wage_bill_selectors.get_manager_wage_bill_total(wage_bill, manager)

    context = {
        'wage_bill': wage_bill,
        'manager_wage_sheets': manager_wage_sheets,
        'manager_total': manager_total,
        'manager': get_user_by_id(manager),
    }

    return render(request, "wage_bill/wage_bill_manager_wagesheets.html", context)
