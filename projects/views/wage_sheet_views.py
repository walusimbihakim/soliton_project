from projects.selectors.complaints import get_complaints
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.contrib import messages

from projects.forms.team_forms import TeamForm
from projects.forms.wage_sheet_forms import WageSheetForm, WageForm
from projects.selectors.teams import get_all_teams, get_team, get_all_pip_teams, get_pip_team
from projects.selectors.wage_sheets import get_all_wage_sheets, get_wage_sheet, get_wages, get_wage, get_submitted_wage_sheets
from projects.selectors.deductions import get_deductions


def manage_wage_sheets_page(request):
    wage_sheets = get_all_wage_sheets()
    form = WageSheetForm()
    if request.method == "POST":
        form = WageSheetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a wage sheet")
        else:
            messages.error(request, "Integrity problems while saving wage sheet")
        return HttpResponseRedirect(reverse(manage_wage_sheets_page))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "wage_sheets": wage_sheets,
        'form': form,
    }
    return render(request, "wage_sheet/manage_wage_sheets.html", context)


def edit_wage_sheet_page(request, id):
    wage_sheet = get_wage_sheet(id)
    form = WageSheetForm(instance=wage_sheet)
    if request.method == "POST":
        form = WageSheetForm(request.POST, request.FILES, instance=wage_sheet)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a wage sheet")
        else:
            messages.error(request, "Integrity problems while saving wage sheet")
        return HttpResponseRedirect(reverse(manage_wage_sheets_page))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage_sheet.html", context)


def delete_wage_sheet(request, id):
    wage_sheet = get_wage_sheet(id)
    wage_sheet.delete()
    messages.success(request, "Successfully deleted a wage sheet")
    return HttpResponseRedirect(reverse(manage_wage_sheets_page))


def manage_wages_page(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    wages = get_wages(wage_sheet_id)
    form = WageForm()
    if request.method == "POST":
        form = WageForm(request.POST, request.FILES)
        if form.is_valid():
            wage = form.save(commit=False)
            wage.wage_sheet = wage_sheet
            wage.save()
            messages.success(request, "Successfully added a wage")
        else:
            messages.error(request, "Integrity problems while saving wage ")
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet_id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "wages": wages,
        "wage_sheet":wage_sheet,
        'form': form,
    }
    return render(request, "wage_sheet/manage_wages.html", context)


def edit_wage_page(request, id):
    wage = get_wage(id)
    wage_sheet = wage.wage_sheet
    form = WageForm(instance=wage)
    if request.method == "POST":
        form = WageForm(request.POST, request.FILES, instance=wage)
        if form.is_valid():
            wage = form.save(commit=False)
            wage.wage_sheet = wage_sheet
            wage.save()
            messages.success(request, "Successfully edited a wage")
        else:
            messages.error(request, "Integrity problems while saving wage")
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet.id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage.html", context)


def delete_wage(request, id):
    wage = get_wage(id)
    wage.delete()
    messages.success(request, "Successfully deleted a wage")
    return HttpResponseRedirect(reverse(manage_wages_page, args=[wage.wage_sheet.id]))

def submit_wage_sheet(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)

    wage_sheet.is_submitted = True
    wage_sheet.save()

    messages.success(request, "Wage Sheet Submitted Successfully")
    return HttpResponseRedirect(reverse(manage_wage_sheets_page))

def view_submitted_wagesheets(request):
    wage_sheets = get_submitted_wage_sheets()

    context = {
        "wage_sheets": wage_sheets,
    }
    return render(request, "wage_sheet/submitted_wage_sheets.html", context)

def manage_submitted_sheet(request, wage_sheet_id, role):

    wage_sheet = get_wage_sheet(wage_sheet_id)
    wages = get_wages(wage_sheet_id)
    complaints = get_complaints(wage_sheet_id)
    deductions = get_deductions(wage_sheet_id)

    context = {
        "wages": wages,
        "wage_sheet": wage_sheet,
        "complaints": complaints,
        "deductions": deductions,
        "role": role,
    }

    return render(request, "wage_sheet/manage_submitted_sheet.html", context)

def approve_reject_wagesheet(request, wagesheet_id):
    if request.method == "POST":
        wage_sheet = get_wage_sheet(wagesheet_id)
        
        role = request.POST.get("role")

        if role == "1":            
            wage_sheet.manager_comment = request.POST.get("wage_comment")
            wage_sheet.manager_status = request.POST.get("wage_action")

            wage_sheet.save()
        
        elif role == "2":
            wage_sheet.project_manager_status = request.POST.get("wage_action")
            wage_sheet.project_manager_comment = request.POST.get("wage_comment")

            wage_sheet.save()
        
        elif role == "3":
            wage_sheet.gm_status = request.POST.get("wage_action")
            wage_sheet.gm_comment = request.POST.get("wage_comment")

            wage_sheet.save()
        
        messages.success(request, "Action saved Successfully")
        
        return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[wagesheet_id, role]))




