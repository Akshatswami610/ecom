from django.contrib import admin
from django.urls import path, include
from .views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', home),  # home page
]
