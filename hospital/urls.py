from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.hospital_register, name='hospital_register'),


    path('login/', views.hospital_login, name='hospital_login'),
    path('logout/', views.hospital_logout, name='hospital_logout'),
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
]