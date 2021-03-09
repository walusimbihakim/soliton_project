from django.shortcuts import render


def django_celery_test(request):
    return render(request, "celery_test/celery_test.html")
