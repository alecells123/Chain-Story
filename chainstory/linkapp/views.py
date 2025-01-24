from django.shortcuts import render
from .models import ChatMessage
from django.http import JsonResponse, HttpResponse

# Create your views here.

def lobby(request):
    return render(request, 'linkapp/lobby.html')

def get_chat_messages(request):
    messages = ChatMessage.objects.all().values('content')
    return JsonResponse({'messages': list(messages)})

def reset(request):
    ChatMessage.objects.all().delete()
    return HttpResponse(status=204)