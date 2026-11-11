from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("painel/", views.exibir_painel, name="painel")
]
