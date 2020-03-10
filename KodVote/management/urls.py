from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
    path('my_poll/', views.my_poll, name='my_poll')
]
