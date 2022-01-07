from django.urls import path, include
from . import views

urlpatterns = [
    path('users/get_image/', views.get_house_img),
    path('users/get_profile/', views.get_profile),
    path('users/update_image/', views.set_house_img),
    path('users/update_profile/', views.update_profile),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]