from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('ping/', views.ping),
    path('api/version/1/', include('authapp.urls'))
]
