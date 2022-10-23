from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('cheese/', views.cheese, name="cheese"),
    path('wine/', views.wine, name="wine"),
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),

]