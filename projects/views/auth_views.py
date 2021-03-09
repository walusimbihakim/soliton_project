from django.shortcuts import render


def super_admin_required_page(request):
    context = {
        "admin": "active",
    }
    return render(request, "auth/super_admin_required.html", context)


def project_manager_required_page(request):
    context = {
        "admin": "active",
    }
    return render(request, "auth/project_manager_required.html", context)


def supervisor_required_page(request):
    context = {
        "admin": "active",
    }
    return render(request, "auth/supervisor_required.html", context)


def finance_officer_required_page(request):
    context = {
        "admin": "active",
    }
    return render(request, "auth/finance_officer_required.html", context)
