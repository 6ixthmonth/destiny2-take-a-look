from django.urls import path

from dbapp import views

app_name = 'dbapp'
urlpatterns = [
    path('update-items/', views.update_items, name='update_items'),
]
