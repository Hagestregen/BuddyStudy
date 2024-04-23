from rest_framework.serializers import ModelSerializer
from base.models import Room


#Converts the content of the model to json format so it can be sent through the API calls
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'