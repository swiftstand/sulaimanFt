from django.shortcuts import render, redirect
from .logics import DashboardLogic




def index(request):

    # Page from the theme
    context = {}
    if request.user.is_authenticated and not request.user.is_superuser:
        context = DashboardLogic().prepare_dashboard(request.user.id, context)

    return render(request, 'pages/index.html', context)


def admin_monitor(request):
    monitor_list = DashboardLogic().prepare_monitor()
    context = {"obj_list" : monitor_list}

    return render(request, "pages/tables.html", context)