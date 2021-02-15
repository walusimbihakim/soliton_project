

from django.shortcuts import render

from projects.tasks import go_to_sleep


def django_celery_test(request):
    result = go_to_sleep.delay(10)
    print(result)
    return render(request, "celery_test/celery_test.html")
