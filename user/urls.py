from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('home', views.home, name="home"),
   path('signup', views.signup, name="signup"),
   path('signin', views.signin, name="signin"),
   path('signout', views.signout, name="signout"),
   path('doctors', views.doctors, name='doctors'),
   path('predict', views.predict, name='predict'),
   path('profile/<str:doctor_username>/', views.view_profile , name='view_profile'),

]