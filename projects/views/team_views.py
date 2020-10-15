from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.contrib import messages

from projects.forms.pip_team_forms import PIPTeamForm
from projects.forms.team_forms import TeamForm
from projects.selectors.teams import get_all_teams, get_team, get_all_pip_teams, get_pip_team


def manage_teams_page(request):
    teams = get_all_teams()
    form = TeamForm()
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a Team")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_teams_page))
    context = {
        "wagebill": "active",
        "manage_teams": "active",
        "teams": teams,
        'form': form,
    }
    return render(request, "team/manage_teams.html", context)


def edit_team_page(request, id):
    team = get_team(id)
    form = TeamForm(instance=team)
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a team")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_teams_page))
    context = {
        "wagebill": "active",
        "manage_teams": "active",
        "form": form,
    }
    return render(request, "team/edit_team.html", context)


def delete_team(request, id):
    team = get_team(id)
    team.delete()
    messages.success(request, "Successfully deleted a team")
    return HttpResponseRedirect(reverse(manage_teams_page))


def manage_pip_team_page(request):
    pip_teams = get_all_pip_teams()
    form = PIPTeamForm()
    if request.method == "POST":
        form = PIPTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a PIP Team")
        else:
            messages.error(request, "Integrity problems while saving worker")
        return HttpResponseRedirect(reverse(manage_pip_team_page))
    context = {
        "wagebill": "active",
        "manage_teams": "active",
        "pip_teams": pip_teams,
        'form': form,
    }
    return render(request, "team/manage_pip_teams.html", context)


def edit_pip_team_page(request, id):
    pip_team = get_pip_team(id)
    form = PIPTeamForm(instance=pip_team)
    if request.method == "POST":
        form = PIPTeamForm(request.POST, request.FILES, instance=pip_team)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a pip team")
        else:
            messages.error(request, "Form is incomplete or invalid")
        return HttpResponseRedirect(reverse(manage_pip_team_page))
    context = {
        "wagebill": "active",
        "manage_teams": "active",
        "form": form,
    }
    return render(request, "team/edit_pip_team.html", context)


def delete_pip_team(request, id):
    team = get_team(id)
    team.delete()
    messages.success(request, "Successfully deleted a pip team")
    return HttpResponseRedirect(reverse(manage_teams_page))
