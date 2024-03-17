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

#Creates a new room and saves it if the input is valid
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

#Method for updating the content of a room
#We enter the primary key to know which item we are updating
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) #What is being updated
    form = RoomForm(instance=room) #Creates a RoomForm instance with the prefilled values from the db
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) #Updates the values of the form under this id
        if form.is_valid():
            form.save() # Saves the values to the db under the id
            return redirect('home') #Returns the user to the home page
    context = {'form': form}
    return render(request, 'base/room_form.html', context) #Context is what is being sent to the html page

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})