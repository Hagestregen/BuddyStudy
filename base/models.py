from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #If a topic is deleted 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #Allows for data to be blank when creating new data
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #Saves the timestamp when data is saved
    created = models.DateTimeField(auto_now_add=True) #Only take a timestamp when the data is created

    #Order the content to display the newest data first
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #When a user is deleted all the children are deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #When parent(Room) is deleted all the messages in the room is deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #Saves the timestamp when data is saved
    created = models.DateTimeField(auto_now_add=True) #Only take a timestamp when the data is created

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50] #Only display the first 50 letters