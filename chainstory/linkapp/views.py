from django.shortcuts import render
from .models import ChatMessage
from django.http import JsonResponse, HttpResponse

# Create your views here.

def lobby(request):
    return render(request, 'linkapp/lobby.html')

def get_chat_messages(request):
    messages = ChatMessage.objects.select_related('user').all()
    message_list = [
        {
            'content': message.content,
            'color': message.color,
            'user': {
                'username': message.user.username,
            }
        }
        for message in messages
    ]
    return JsonResponse({'messages': message_list})

def reset(request):
    ChatMessage.objects.all().delete()
    return HttpResponse(status=204)