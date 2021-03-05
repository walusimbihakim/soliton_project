from django.shortcuts import render


def super_admin_required_page(request):
    context = {
        "admin": "active",
    }
    return render(request, "auth/super_admin_required.html", context)