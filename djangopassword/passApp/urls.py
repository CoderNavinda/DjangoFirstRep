from django.urls import path
from passApp import views

app_name = 'passApp'

urlpatterns = [
path('register/', views.register, name = 'register'),
path('login/', views.user_login, name = 'user_login')

]
