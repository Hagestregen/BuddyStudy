from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Python key value pair
# rooms = [
#     {'id': 1, 'name': 'Learn how not to code in python!'},
#     {'id': 2, 'name': 'Destroy code with me!'},
#     {'id': 3, 'name': 'No-end developers'},
# ]

# Take in a request from url:''
# Return the base/home.html with the values from rooms
# The context var is passed to the home.html site and displayed on the page by using a for loop
def home(request):
    rooms = Room.objects.all() # gives us all the objects in the db
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk) # gives us the object with id matching the pk
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)
