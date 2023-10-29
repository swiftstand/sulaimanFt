from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/monitor', views.admin_monitor, name='user_monitor'),
]
