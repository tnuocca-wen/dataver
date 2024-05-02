from django.urls import path
from . import views

app_name = 'datavalidation'
urlpatterns = [
    path("", views.index, name ="index"),
    path('text/', views.textpair, name='textpair'),
    path('yesorno/', views.yon, name='yesorno'),
    path('edit/', views.edittext, name='edit'),
    ]