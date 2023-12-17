from django.urls import path

from d2api import views

app_name = 'd2api'
urlpatterns = [
    path('get-events/', views.get_events, name='get_events'),
    path('get-manifest/', views.get_manifest, name='get_manifest'),
    path('get-definition/', views.get_definition, name='get_definition'),
    path('get-auth/', views.get_auth, name='get_auth'),
    path('fetch-token/', views.fetch_token, name='fetch_token'),
    path('get-vendor-data/', views.get_vendor_data, name='get_vendor_data'),
    path('get-limited-time-vendor-Data/', views.get_limited_time_vendor_data, name='get_limited_time_vendor_data'),
    # path('update-item/', views.update_item, name='update_item'),
    path('predict-item/', views.predict_item, name='predict_item'),
]
