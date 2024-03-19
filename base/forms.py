from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants'] #This will make sure the host and participants are not sent when creating a new room 'form'. We now have to change the view method to save the user:'host' to the room form