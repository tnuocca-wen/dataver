from django.urls import path
from . import views

app_name = 'data'
urlpatterns = [
    path("upload/", views.adddata, name ="upload"),
    path("export/<str:file_name>", views.exportdata, name ="export"),
    ]