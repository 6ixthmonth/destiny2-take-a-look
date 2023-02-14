from django.urls import path

from d2api import views

app_name = 'd2api'
urlpatterns = [
    path('getAuth/', views.get_auth, name='get_auth'),
    path('fetchToken/', views.fetch_token, name='fetch_token'),
    path('refreshToken/', views.refresh_token, name='refresh_token'),
    path('requestData/', views.request_data, name='request_data')
]
