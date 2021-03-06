from django.contrib.admin.views.decorators import staff_member_required
from django.core.checks import messages
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.views.generic.edit import UpdateView

from users.forms import CustomUserCreationForm
from .forms import ClubCreationForm, StudentClubRelationCreationForm, EditUserForm


from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from users.models import CustomUser
from main.models import Club, StudentClubRelation, Portfolio


# Redirect user to login page if not logged in
@login_required(login_url='/accounts/login/')
def manage_users(request):
    # Display users
    # username_list = CustomUser.objects.all().values_list('username', flat=True),
    user_list = list(CustomUser.objects.filter(is_active=True)) # i.e if user has been deleted or not
    if request.method == 'POST':
        if 'remove' in request.POST:
            selected = request.POST.getlist("selected")
            for username in selected:
                curr_user = CustomUser.objects.get(username=username)
                curr_user.is_active = False
                curr_user.save()
                # curr_user.set
            temp = ""
            return redirect(manage_users)
    # usernames = user_list.values_list('username', flat=True),
    # return HttpResponse(template.render(context, request))
    # , 'usernames': usernames} 'username_list': username_list,
    return render(request, 'administration/manage_users.html', {'user_list': user_list})


def create_user(request):
    # User creation
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # username = form.cleaned_data.get('username') # May cause issues
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            # first_name = form.data.get('first_name')
            # last_name = form.data.get('last_name')
            # email = form.data.get('email')
            # contact_number = form.data.get('contact_number')
            # id_number = form.data.get('id_number')
            # dob = str(id_number)[:6]
            # raw_password = dob  # Will be changed below

            # If this user exists but has been 'deleted" previously reset is_active to true
            # if CustomUser.objects.filter(username=username).exists():
            #     curr_user = CustomUser.objects.filter(username=username)
            #     if curr_user.is_active:
            #         print(curr_user.username + " already exists, cannot add")
            #         messages.error(request, curr_user.username + " already exists, cannot add")
            #     else:
            #         curr_user.is_active = True
            # else:
            #     pass

            curr_user = CustomUser.objects.create_user(username=username)
            # curr_user = CustomUser.objects.create_user(username=username, password=raw_password, email=email, first_name=first_name, last_name=last_name, contact_number=contact_number, id_number=id_number)
            # curr_user = authenticate(username=username, password=raw_password)
            # basically says that the user has no password - used for custom authentication i.e. LDAP
            # curr_user.set_unusable_password()
            curr_user.save()
            # redirect back to manage_users
            return redirect(manage_users)
        # elif CustomUser.objects.filter(username=username).exists():
        #     curr_user = CustomUser.objects.filter(username=username)
        #     if curr_user.is_active:
        #         messages.error(request, curr_user.username + " already exists")
        #     else:
        #         curr_user.is_active = True
        #         print(curr_user.username + " re-added")
    else:
        form = CustomUserCreationForm()
    return render(request, 'administration/create_user.html', {'form': form})


# instead of deleting a user to avoid issues with the database - rather delete for the moment
# def deactivate_user(request, username):
#     obj = CustomUser.objects.get(pk=username)
#     obj.is_active = False
#     obj.save()
#     return render(request, 'administration/manage_users.html')


# Don't think this is used
def user(request, user_id):
    currUser = CustomUser.objects.get(username=user_id)
    return render(request, 'administration/user.html', {user: currUser})
    # return HttpResponse("You're looking at user %s." % user_id)


def edit_user(request, user_id):
    instance = get_object_or_404(CustomUser, username=user_id)
    curr_user = CustomUser.objects.get(username=user_id)
    form = EditUserForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('manage_users')
    return render(request, 'administration/edit_user.html', {'form': form, 'currUser': curr_user})


# class edit_user_view(UpdateView):
#     model = CustomUser
#     fields = ['username']
#     template_name = 'administration/edit_user.html'


def manage_clubs(request):
    # clubs = Club.objects.all()
    clubs = list(Club.objects.filter(is_deleted=False))
    if request.method == 'POST':
        if 'remove' in request.POST:
            selected = request.POST.getlist("selected")
            for club_id in selected:
                curr_club = Club.objects.get(club_id=club_id)
                curr_club.is_deleted = True
                curr_club.save()
                # curr_user.set
            temp = ""
            return redirect(manage_clubs)
    return render(request, 'administration/manage_clubs.html', {'clubs': clubs})


def club(request, club_id):
    currClub = Club.objects.get(club_id=club_id)
    club_id = club_id
    studentClubRelations = StudentClubRelation.objects.filter(club_id=club_id, is_deleted=False)
    # Make this work...
    if request.method == 'POST':
        if 'remove' in request.POST:
            selected = request.POST.getlist("selected")
            for curr_id in selected:
                curr_scr= StudentClubRelation.objects.get(id=curr_id)
                curr_scr.is_deleted = True
                curr_scr.save()
                # curr_user.set
            temp = ""
            return redirect(club, club_id)
        else:
            form = StudentClubRelationCreationForm(request.POST,club_id = club_id)
            # kwargs = form.get_form_kwargs()
            # kwargs.update({'club_id': club_id})
            # form.fields.club_id
            if form.is_valid():
                form.save(commit=False)
                user = CustomUser.objects.get(pk=form.data.get('user_id'))
                portfolio = Portfolio.objects.get(pk=form.data.get('portfolio_id'))
                # Dunno if this is valid
                curr_studentClubRelation = StudentClubRelation(user_id=user, portfolio_id=portfolio, club_id= currClub)
                # curr_user = authenticate(username=username, password=raw_password)
                # basically says that the user has no password - used for custom authentication i.e. LDAP
                # curr_user.set_unusable_password()
                curr_studentClubRelation.save()
                # return redirect(manage_clubs)
    else:
        form = StudentClubRelationCreationForm()
    return render(request, 'administration/club.html', {'club': currClub, 'studentClubRelations': studentClubRelations, 'form': form})

    # def get_form_kwargs(self):
    #     kwargs = super(club, self).get_form_kwargs()
    #     kwargs.update({'club_id': self.club_id})
    #     return kwargs


def create_club(request):
    if request.method == 'POST':
        form = ClubCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(manage_clubs)
    else:
        form = ClubCreationForm()
    return render(request, 'administration/create_club.html', {'form': form})


# class DeleteClub(DeleteView):
#     model = Club








