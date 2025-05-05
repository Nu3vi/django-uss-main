from django.urls import path
from . import views
from .views import HolaMundoAPIView

urlpatterns = [
    path('', views.hola_mundo),
    path('api/hola/', HolaMundoAPIView.as_view())
]
