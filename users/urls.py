from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gauth/', views.gauth, name='gauth'),
]
