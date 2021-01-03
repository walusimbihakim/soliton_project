from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.contrib import messages

from projects.forms.team_forms import TeamForm
from projects.selectors.teams import get_all_teams, get_team, get_all_pip_teams, get_pip_team
from projects.selectors.wage_sheets import get_wage_sheet
from projects.selectors.complaints import get_complaints, get_complaint
from projects.forms.complaint_forms import ComplaintForm


def manage_complaints_page(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    complaints = get_complaints(wage_sheet_id)
    form = ComplaintForm()
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.wage_sheet = wage_sheet
            complaint.save()
            messages.success(request, "Successfully added a complaint")
        else:
            messages.error(request, "Integrity problems while saving complaint ")
        return HttpResponseRedirect(reverse(manage_complaints_page, args=[wage_sheet_id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "complaints": complaints,
        "wage_sheet":wage_sheet,
        'form': form,
    }
    return render(request, "wage_sheet/manage_complaints.html", context)


def edit_complaint_page(request, id):
    complaint = get_complaint(id)
    wage_sheet = complaint.wage_sheet
    form = ComplaintForm(instance=complaint)
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.wage_sheet = wage_sheet
            complaint.save()
            messages.success(request, "Successfully edited a complaint")
        else:
            messages.error(request, "Integrity problems while saving complaint")
        return HttpResponseRedirect(reverse(manage_complaints_page, args=[wage_sheet.id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_complaint.html", context)


def delete_complaint(request, id):
    complaint = get_complaint(id)
    complaint.delete()
    messages.success(request, "Successfully deleted a complaint")
    return HttpResponseRedirect(reverse(manage_complaints_page,
                                        args=[complaint.wage_sheet.id]))
