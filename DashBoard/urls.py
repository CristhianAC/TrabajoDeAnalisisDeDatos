from django.urls import path
from DashBoard import views

urlpatterns = [
    path('', views.index),
    #path('DashBoard', views.proyect),
]