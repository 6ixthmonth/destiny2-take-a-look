from django.urls import path

from d2api import views

urlpatterns = [
    path('req/', views.req)
]
