from django.urls import path

from d2api import views

app_name = 'd2api'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('get-manifest/', views.get_manifest, name='get_manifest'),
    path('get-auth/', views.get_auth, name='get_auth'),
    path('fetch-token/', views.fetch_token, name='fetch_token'),
    path('get-data/', views.get_data, name='get_data'),
    path('get-limited-time-vendor-Data/', views.get_limited_time_vendor_data, name='get_limited_time_vendor_data'),
]
