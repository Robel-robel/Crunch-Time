from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from message_board.models import Message
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import datetime
import users.models
import main.models
from users.models import CustomUser
from main.models import StudentClubRelation, Club, Portfolio
from django.core.mail import send_mail

# Create your views here.

# Redirect user to login page if not logged in
@login_required(login_url='/accounts/login/')

def messageBoard(request):

    messageBoardNames = []
    curr_user = request.user
    studentClubEntities = StudentClubRelation.objects.filter(user_id=curr_user)
    # studentClubEntities = main.models.StudentClubRelation(user_id=curr_user).objects.all()
    for entity in studentClubEntities:
        # user = CustomUser.objects.get(pk=form.data.get('user_id'))
        clubName = Club.objects.get(club_id=entity.club_id.club_id).club_name
        # portfolioName = main.models.Portfolio(position_id=entity.position_id).objects.first().portfolio_name
        # No idea if following will work
        portfolioName = Portfolio.objects.filter(portfolio_id = entity.portfolio_id.portfolio_id).first().portfolio_name
        if clubName not in messageBoardNames:
            messageBoardNames.append(clubName)
        if portfolioName not in messageBoardNames:
            messageBoardNames.append(portfolioName)

    url = request.get_full_path(False)

    messageBoard = ''
    i = url.find('=')
    if i == -1:
        messageBoard = "main"
    else:
        messageBoard = url[i + 1:]

    messages = Message.objects.filter(message_board_name=messageBoard)

    if not (request.user.is_superuser or request.user.is_staff):
        # your logic here
        return redirect("mainMessageBoardView")  # or your url name

    return render(request, 'message_board/Admin_message_board.html', {'messages': messages, 'messageboards': messageBoardNames, 'messageboard': messageBoard})


def Messages(request):
    return render(request, 'Messages/messages.html')


def MainMessages(request):
    # return render(request, 'message_board/Main_Message_Board.html')

    messageBoardNames = []
    curr_user = request.user
    studentClubEntities = StudentClubRelation.objects.filter(user_id=curr_user)
    # studentClubEntities = main.models.StudentClubRelation(user_id=curr_user).objects.all()
    for entity in studentClubEntities:
        # user = CustomUser.objects.get(pk=form.data.get('user_id'))
        clubName = Club.objects.get(club_id=entity.club_id.club_id).club_name
        # portfolioName = main.models.Portfolio(position_id=entity.position_id).objects.first().portfolio_name
        # No idea if following will work
        portfolioName = Portfolio.objects.filter(portfolio_id = entity.portfolio_id.portfolio_id).first().portfolio_name
        if clubName not in messageBoardNames:
            messageBoardNames.append(clubName)
        if portfolioName not in messageBoardNames:
            messageBoardNames.append(portfolioName)

    url = request.get_full_path(False)

    messageBoard = ''
    i = url.find('=')
    if i == -1:
        messageBoard = "Main"
    else:
        messageBoard = url[i + 1:]

    messages = Message.objects.filter(message_board_name=messageBoard)

    return render(request, 'Messages/messages.html', {'messages': messages, 'messageboards': messageBoardNames, 'messageboard': messageBoard})

# def messageBoard(request):
#     messages = Message.objects.all()
#     return render(request, 'message_board/Admin_message_board.html', {messages: messages})
#
# def Messages(request):
#     messages = Message.objects.all()
#     return render(request, 'Messages/messages.html', {messages : messages})

# def ManageUsers(request):
#     return render(request, 'message_board/Create_Users.html')
#
# def ManageClubs(request):
#     return render(request, 'message_board/Customise_Clubs.html')
#
# def CustomiseUsers(request):
#     return render(request, 'message_board/Customise_Users.html')


def SendMessage(request):
    if request.method == 'POST':
        if request.POST.get('header') and request.POST.get('body'):
            message = Message()
            message.message_header = request.POST.get('header')
            message.message_body = request.POST.get('body')
            message.user = users.models.CustomUser.objects.first()
            message.date_time = datetime.datetime.now()

            url = request.get_full_path(False)
            messageBoard = ''
            i = url.find('=')
            if i == -1:
                messageBoard = "Main"
            else:
                messageBoard = url[i + 1:]
            message.message_board_name = messageBoard

            message.save()

            # send message as email to all users of this message board

            if messageBoard == "main" or messageBoard == "Main" or messageBoard == "MAIN":
                studClubEntities = StudentClubRelation.objects.all()
            else:
                clubEntity = Club.objects.filter(club_name=messageBoard).first()
                if clubEntity is not None:
                    club_id = clubEntity.club_id
                    studClubEntities = StudentClubRelation.objects.filter(club_id=club_id).all()
                else:
                    portfolio_id = Portfolio.objects.filter(portfolio_name=messageBoard).first().portfolio_id
                    studClubEntities = StudentClubRelation.objects.filter(portfolio_id=portfolio_id).all()

            myUsers = []
            for entity in studClubEntities:
                myUsers.append(entity.user_id.email)

            send_mail(
                message.message_header,
                message.message_body,
                message.user.email,
                myUsers,
                fail_silently=True,
                auth_user=message.user.email,
                auth_password=request.POST.get('email_password')
            )

            return redirect(reverse('messageBoardView') + '?messageboard=' + messageBoard)
    return render(request, 'message_board/Send_Message.html')


def MessageBoard(request):

    messageBoardNames = []
    curr_user = request.user
    studentClubEntities = StudentClubRelation.objects.filter(user_id=curr_user)
    # studentClubEntities = main.models.StudentClubRelation(user_id=curr_user).objects.all()
    for entity in studentClubEntities:
        # user = CustomUser.objects.get(pk=form.data.get('user_id'))
        clubName = Club.objects.get(club_id=entity.club_id.club_id).club_name
        # portfolioName = main.models.Portfolio(position_id=entity.position_id).objects.first().portfolio_name
        # No idea if following will work
        portfolioName = Portfolio.objects.filter(portfolio_id = entity.portfolio_id.portfolio_id).first().portfolio_name
        if clubName not in messageBoardNames:
            messageBoardNames.append(clubName)
        if portfolioName not in messageBoardNames:
            messageBoardNames.append(portfolioName)

    return render(request, 'message_board/Main_Message_Board.html')


# def CustomiseClubs(request):
#     return render(request, 'message_board/Customise_Clubs.html')


# def MainMessages(request):
#     return render(request, 'message_board/Main_Message_Board.html')

# def UserProfile(request):
#     return render(request, 'message_board/User_Profile.html')
#
# def WSCHeader(request):
#     return render(request, 'WSCHeader.html')
#
def ChairPerson(request):
    return render(request, 'message_board/Chair-Person-Messages.html')

def ViceChairPerson(request):
    return render(request, 'message_board/Vice-Chair-Person-Messages.html')

def Treasurer(request):
    return render(request, 'message_board/Treasurer-Messages.html')
