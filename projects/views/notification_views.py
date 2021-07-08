from django.shortcuts import render

from projects.services.notification_services import read_all_notifications


def unread_notifications_page(request):
    return render(request, "notification/unread_notifications.html")


def notifications_page(request):
    read_all_notifications(request.user.unread_notifications)
    return render(request, "notification/all_notifications.html")
