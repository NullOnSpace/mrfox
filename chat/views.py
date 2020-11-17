from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Author

# Create your views here.
@login_required
def room(request, room_id):
    rm = {'id': room_id}
    return render(request, 'chat/chatroom.html', {
        'room': rm,
    })


@login_required
def contact(request):
    u = request.user
    contacts = [{
        'dest': f"user_{a.id}_{u.id}" if a.id<u.id else f"user_{u.id}_{a.id}",
        "name": a.username
        }
        for a in Author.objects.all() if a != u]
    return render(request, 'chat/contact.html', {
        'contacts': contacts,
    })
