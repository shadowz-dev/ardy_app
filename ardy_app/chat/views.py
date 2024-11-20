# chat/views.py
from django.shortcuts import render

# Create your views here.

def chat_room(request, project_id):
    return render(request, 'chat/room.html', {
        'project_id': project_id,
    })