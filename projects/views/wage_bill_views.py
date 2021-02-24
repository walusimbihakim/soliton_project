from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import datetime

import projects.models.wage_bills as wage_bills
import projects.forms.wage_bill_forms as wage_bill_forms
import projects.selectors.wage_bill_selectors as wage_bill_selectors
import projects.selectors.wage_sheets as wage_sheet_selectors

def manage_wage_bill(request):
    wage_bill_form = wage_bill_forms.WageBillForm()

    if request.method == "POST":
        wage_bill_form = wage_bill_forms.WageBillForm(request.POST, request.FILES)

        if wage_bill_form.is_valid():
            current_wage_bill = wage_bill_selectors.get_current_wage_bill()
            current_wage_bill.status = "Done"
            current_wage_bill.save()
            wage_bill_form.save()

            messages.success(request, "Wage Bill Record Saved Successfully")
        
        else:
            messages.warning(request, "Something went wrong, check your Input and try again")
    
    wagebills = wage_bill_selectors.get_wage_bills()

    context = {
        "wagebills": wagebills,
        "wage_bill_form": wage_bill_form
    }
    return render(request, "wage_bill/manage_wage_bill.html", context)

def edit_wage_bill(request, wage_bill_id):
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    wage_bill_form = wage_bill_forms.WageBillForm(instance = wage_bill)

    if request.method == "POST":
        wage_bill_form = wage_bill_forms.WageBillForm(request.POST, request.FILES, instance = wage_bill)

        if wage_bill_form.is_valid():
            wage_bill_form.save()

            messages.success(request, "Changes Saved Successfully")
        
        else:
            messages.error(request, "Something went wrong, check your Input and try again")
        return HttpResponseRedirect(reverse(manage_wage_bill))
    context = {
        "wagebill": "active",
        "manage_wage_bill": "active",
        # "wage_bill": wage_bill,
        "wage_bill_form": wage_bill_form,
    }
    return render(request, "wage_bill/edit_wage_bill.html", context)

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

def consolidated_wage_bill(request):
    wage_bill = wage_bill_selectors.get_current_wage_bill()
    wages =wage_bill_selectors.get_wage_bill_wages(wage_bill)
    
    aggregated_wages = wage_bill_selectors.get_aggregated_wage_bill(wage_bill)
        
    context = {
        "wage_bill": wage_bill,
        "wages": wages,
        "aggregated_wages": aggregated_wages,
    }

    return render(request, "wage_bill/consolidated_wage_bill.html", context)
