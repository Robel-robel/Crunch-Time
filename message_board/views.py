from django.shortcuts import render

# Create your views here.


def MessageBoard(request):
    return render(request, 'message_board/message_board.html')

def Messages(request):
    return render(request, 'Messages/messages.html')