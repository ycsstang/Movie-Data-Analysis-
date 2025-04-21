from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('catChart/', views.catChart, name='catChart'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('countryChart/', views.countryChart, name='countryChart'),
    path('timeChart/', views.timeChart, name='timeChart'),
    path('ticketChart/', views.ticketChart, name='ticketChart'),
    path('totalMovies/', views.totalMovies, name='totalMovies'),
]

