from django.urls import path

from apitest import views

urlpatterns = [
    path('conntest/', views.conntest)
]