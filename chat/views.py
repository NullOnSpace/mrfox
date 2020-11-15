from django.shortcuts import render


# Create your views here.
def room(request, room_id):
    rm = {'id': 1}
    return render(request, 'chat/chatroom.html', {
        'room': rm,
    })
