from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #Takes in a str id that is a parameter in the view: room method
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room', views.createRoom, name='create-room')
]