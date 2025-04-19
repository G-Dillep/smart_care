from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register_doctor, name='register_doctor'),
    path('doctors/', views.doctor_details, name='doctor_details'),
]