from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    

    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('room/<str:pk>/', views.room, name='room'), #Takes in a str id that is a parameter in the view: room method
    
    
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'), #Update room need a pk for the function 'updateRoom'
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),

    path('edit-user/', views.updateUser, name='edit-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
]