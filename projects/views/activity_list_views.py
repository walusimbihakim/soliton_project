from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import JsonResponse

from projects.forms.activity_list_form import *
from projects.selectors.activity_selectors import *


def activity_page_view(request):
    activity_form = ActivityListForm(request.POST, request.FILES)

    if request.method == "POST":
        if activity_form.is_valid():
            activity_form.save()

            messages.success(request, "Successfully added activity")
            return HttpResponseRedirect(reverse(activity_page_view))

    activities = get_activities()

    context = {
        "activities": activities,
        "activity_form": activity_form,
    }

    return render(request, "activity/activity_list.html", context)


def edit_activity_view(request, activity_id):
    activity = get_activity(activity_id)

    activity_form = ActivityListForm(instance=activity)

    if request.method == "POST":
        activity_form = ActivityListForm(request.POST, instance=activity)
        if activity_form.is_valid():
            activity_form.save()

            messages.success(request, "Changes saved Successfully")
            return HttpResponseRedirect(reverse(activity_page_view))

    context = {
        "projects": "active",
        "activity_list": "active",
        "activity_form": activity_form,
        "activity": activity,
    }
    return render(request, 'activity/edit_activity_list.html', context)


def delete_activity_view(request, activity_id):
    activity = get_activity(activity_id)

    activity.delete()

    messages.success(request, "Successfully Deleted activity")
    return HttpResponseRedirect(reverse(activity_page_view))


def get_activity_rate(request):
    activity_id = request.GET['activity_id']
    activity = get_activity(activity_id)
    activity_rate = activity.unit_cost
    return JsonResponse({'success': True, 'activity_rate': activity_rate})
