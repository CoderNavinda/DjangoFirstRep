from django.shortcuts import render
from passApp.forms import UserForm,UserProfileInfoForm

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate,login, logout


# Create your views here.
def index(request):
    return render(request,'passApp/index.html',{'hello':'hello'})


@login_required
def special(request):
    return HttpResponse('You are Logged in')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered =  False
    if request.method == 'POST':
        User_form = UserForm(data = request.POST)
        UserProfileInfo_form = UserProfileInfoForm(data = request.POST)

        if User_form.is_valid() and UserProfileInfo_form.is_valid():
            user = User_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfileInfo_form.save(commit = False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic =request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(User_form.errors,UserProfileInfo_form.errors)
    else:
        User_form = UserForm()
        UserProfileInfo_form = UserProfileInfoForm()


    return render(request,'passApp/registrations.html',{'registered': registered, 'User_form': User_form, 'UserProfileInfo_form': UserProfileInfo_form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('some one tried to login to {} with {}'.format(username,password))
            return HttpResponse('login detals wrong')
    else:
        return render(request,'passApp/login.html',{})
