from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # La URL raíz apuntará a index
]