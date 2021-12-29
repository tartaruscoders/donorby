from django.urls import path
from . import views

urlpatterns = [
    path('login', views.HospitalLogin, name="HospitalLogin"),
    path('registration', views.HospitalRegister, name="HospitalRegister"),
    path('home', views.HospitalMain, name="HospitalMain" ),
    path('map', views.MapDistanceCalculate, name="MapDistanceCalculate")
]
 