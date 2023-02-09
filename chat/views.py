from django.shortcuts import render
from .forms import MessageForm
from django.views import View

from .models import Room, Message
from accounts.models import Account
# Create your views here.


def privateChat(request, room_slug):
    chat_room = Room.objects.get(slug=room_slug)
    sent_messages = Message.objects.filter(
        sender=request.user, recipient=chat_room.owner).order_by('created')
    received_messages = Message.objects.filter(
        recipient=request.user, sender=chat_room.owner).order_by('created')
    users = Account.objects.exclude(username=request.user.username)
    messages = sent_messages | received_messages

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = chat_room.owner
            message.save()
    else:
        form = MessageForm()

    return render(request, 'chat/chat.html', {'form': form, 'chat_room': chat_room, 'messages': messages, 'users': users})
