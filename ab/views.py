from django.shortcuts import render

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from .models import *
from django.contrib.auth.models import User

from ab.forms import *

import pandas as pd
def index(request):
    return render(request, 'index.html')

def userdash(request):
    if request.method == 'POST':
        print("amitaaaaaaaaaaaaaaaaaaaaaaaaa")
        excel_file = request.FILES["fileToUpload"]
        print(excel_file,'fileeeeeeeeeeeeeee')
        df=pd.read_csv(excel_file)
        print(df)
        return HttpResponse(df.to_html())
    return render(request, 'userdashboard.html')

# def signup_page(request):
#   if request.method == 'POST':
#       usename = request.POST['u-name']
#       password = request.POST['psw']
#       email = request.POST['email']
#       fname = request.POST['f-name']
#       lname = request.POST['l-name']
#       data=[fname,lname,email,usename,password]
#       if password and usename:
#           try:
        
#               user = User.objects.create_user(username=usename, password=password,email=email,first_name=fname,last_name=lname)
#               r = user.save()
        
#               if r is None:
#                   return HttpResponse('45')
#           except: 
#               return render(request,'signup.html',{'data':data})
#       else:
#         print("create_user does not contain fields")
#         return render(request,'registration_form.html')

#   return render(request,'signup.html')


# def login_user(request):
#   if request.method != 'POST':
#       return render(request,'signin.html')
#   username = request.POST['js']
#   password = request.POST['aak']
#   user  = authenticate(username=username.lower(), password=password)
#   if user is not None:
#       if user.is_active:
#           login(request, user)
#           return HttpResponse('successfully login')
#       else:
#           return HttpResponse("Your account is disabled.")
#   else:
#       return redirect('/register/')



def signup_page(request):
    if request.method=="POST":
        form=signupform(request.POST)
        if form.is_valid():
            name=request.POST["Name"]
            email=request.POST["Email"]
            password=request.POST["Password"]
            Firstname=request.POST["Firstname"]
            lastname=request.POST["lastname"]
            user = User.objects.create_user(username=name,email=email,password=password,first_name=Firstname,last_name=lastname)
            user.save()
            return redirect('/signin/')
    else:
        form = signupform()
        print("notdshksfdhjsdfhsdfahlsafd")
    return render(request,'signup.html',{"form":form})



def login_user(request):
    if request.user.is_authenticated:
        print("Logged in")
        return redirect("/userdash/")
    else:
        print("Not logged in")

    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = request.POST.get('Username')
            print(username)
            password = request.POST.get('Password')
            print(password)
            user = authenticate(username=username, password=password)
            if user:
                print("yesssssssssssssssss")
                login(request,user)
                return redirect("/userdash/")

    else:
        form = loginform()
        print("not")
    return render(request, 'signin.html', {"form": form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('/signin/')



def read(request):
    
    return redirect("/userdash/")



