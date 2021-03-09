from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse

from projects.forms.segment_forms import SegmentForm
from projects.selectors.segments import get_all_segments, get_segment


def manage_segments_page(request):
    segments = get_all_segments()
    form = SegmentForm()
    if request.method == "POST":
        form = SegmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added a segment")
        else:
            messages.error(request, "Integrity problems while saving a segment")
        return HttpResponseRedirect(reverse(manage_segments_page))
    context = {
        "wagebill": "active",
        "manage_segments": "active",
        "segments": segments,
        'form': form,
    }
    return render(request, "segment/manage_segments.html", context)


def edit_segment_page(request, id):
    segment = get_segment(id)
    form = SegmentForm(instance=segment)
    if request.method == "POST":
        form = SegmentForm(request.POST, request.FILES, instance=segment)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a segment")
        else:
            messages.error(request, "Integrity problems while saving a segment")
        return HttpResponseRedirect(reverse(manage_segments_page))
    context = {
        "wagebill": "active",
        "manage_segments": "active",
        "form": form,
    }
    return render(request, "segment/edit_segment.html", context)


def delete_segment(request, id):
    segment = get_segment(id)
    segment.delete()
    messages.success(request, "Successfully deleted a segment")
    return HttpResponseRedirect(reverse(manage_segments_page))
