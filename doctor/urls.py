from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_doctor, name='register_doctor'),
    path('doctors/', views.doctor_details, name='doctor_details'),


    
    path('login/', views.doctor_login, name='doctor_login'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('logout/', views.doctor_logout, name='doctor_logout'),
]