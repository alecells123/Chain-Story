from django.urls import path
from . import views

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('api/chat/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('reset', views.reset, name='reset')
]