from django.urls import path

from d2api import views

app_name = 'd2api'
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin, name='admin'),
    path('getAuth/', views.get_auth, name='get_auth'),
    path('fetchToken/', views.fetch_token, name='fetch_token'),
    path('requestData/', views.request_data, name='request_data')
]
