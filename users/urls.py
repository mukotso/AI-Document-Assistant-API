from django.urls import path
from .views import register, login, get_all_users

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('all/', get_all_users, name='get_all_users'),
]
