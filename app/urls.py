from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name="home"),
    path('prediction', views.prediction, name="prediction"),
    path('geneticAlgo', views.geneticAlgo, name="geneticAlgo"),
]