from django.shortcuts import render

def index(request):
    return render(request, 'ws_chat/index.html')

def chat(request):
    username = request.GET.get('username', 'Annoymous')
    return render(request, 'ws_chat/chat.html', {'username': username})
