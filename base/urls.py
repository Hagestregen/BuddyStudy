from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    #Takes in a str id that is a parameter in the view: room method
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'), #Update room need a pk for the function 'updateRoom'
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
]