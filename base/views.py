from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Python key value pair
# rooms = [
#     {'id': 1, 'name': 'Learn how not to code in python!'},
#     {'id': 2, 'name': 'Destroy code with me!'},
#     {'id': 3, 'name': 'No-end developers'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) #This logs the user in and creates a session
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request) #Deletes the user session
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #Freeze the save so that we can use lowercase on username
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home') #The registered user is logged in
        else:
            messages.error(request, 'An error occured')
    return render(request, 'base/login_register.html', {'form':form})


# Take in a request from url:''
# Return the base/home.html with the values from rooms
# The context var is passed to the home.html site and displayed on the page by using a for loop
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' #q is equal to whatever we pass into the url
    rooms = Room.objects.filter(  #Check if a object contain the value in q and set that to 'room', the Q allows us to check if q is in multiple fields
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count() #Gives us the number of rooms
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #Only display the messages with context to room
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
                'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk) # gives us the object with id matching the pk
    room_messages = room.message_set.all().order_by('-created') #Gives us the info about the Message model as a child of Room model in a order of newest first
    participants = room.participants.all()
    

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages':room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() #Gives us all the children of a object by giving the model name: 'room', and '_set'
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms': rooms, 'topics':topics, 'room_messages':room_messages}
    return render(request, 'base/profile.html', context)


#Creates a new room and saves it if the input is valid
@login_required(login_url='login') #Requires user to be logged in to access this function, if not the user is redirected to the login page
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
@login_required(login_url='login') #Requires user to be logged in to access this function, if not the user is redirected to the login page
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) #What is being updated
    form = RoomForm(instance=room) #Creates a RoomForm instance with the prefilled values from the db
    if request.user != room.host: #Check if user is the creator of the room, if not the httpresponse will be triggered
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) #Updates the values of the form under this id
        if form.is_valid():
            form.save() # Saves the values to the db under the id
            return redirect('home') #Returns the user to the home page          
    context = {'form': form}
    return render(request, 'base/room_form.html', context) #Context is what is being sent to the html page


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})