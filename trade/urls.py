from django.urls import path

from . import views

urlpatterns = [
    path('simulate/<int:user_pk>/', views.simulate_trading, name='simulate'),
]
