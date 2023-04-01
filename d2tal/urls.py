from django.contrib import admin
from django.urls import include, path
from d2tal.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('d2api/', include('d2api.urls')),
]
