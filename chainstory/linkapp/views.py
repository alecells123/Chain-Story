from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage, User

# Create your views here.

def lobby(request):
    return render(request, 'linkapp/lobby.html')

def get_chat_messages(request):
    messages = ChatMessage.objects.select_related('user').all().order_by('timestamp')
    return JsonResponse({
        'messages': [{
            'content': msg.content,
            'color': msg.color,
            'username': msg.user.username
        } for msg in messages]
    })

def reset(request):
    if request.method == 'POST':
        User.objects.all().delete()
        return JsonResponse({}, status=204)
    return JsonResponse({}, status=405)