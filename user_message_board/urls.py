from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainMessages, name='mainMessageBoardView'),
    path('messages.html', views.Messages, name='UserMessage'),  # Don't know if this is actually used...
    # path('Main_Message_Board.html', views.MainMessages),
    # path('Create_Users.html', views.ManageUsers),
    # path('Manage_Clubs.html', views.ManageClubs)
    # arguments for path function -
    # route (required)
    # view (required)
    # kwargs - Arbitrary keyword arguments can be passed in a dictionary to the target view
    # name - lets you refer to it unambiguously from elsewhere in Django
]

