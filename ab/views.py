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
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

def index(request):
    return render(request, 'index.html')

def userdash(request):
    if request.method == 'POST':
        if request.POST.get("read"):
            print('amitaaaaaaaaaaaaa')
            excel_file = request.FILES["fileToUpload"]

            print(type(excel_file),"excel_fileexcel_fileexcel_fileexcel_file")
            print(excel_file,"excel_fileexcel_fileexcel_fileexcel_fileexcel_file")
            print(excel_file,'fileeeeeeeeeeeeeee')
            df=pd.read_excel(excel_file)
            print(df)
            print(df)
            data_top = df.columns
            data_top=list(data_top)
            print("headers",data_top)

            return render(request, 'userdashboard.html',{"data":data_top,'file':excel_file})
        if request.POST.get("show"):
            column_names=[]
            excel_file = request.FILES["fileToUpload"]
            col = request.POST["col"]
            column_names.append(str(col))
            inc = request.POST["inc"]
            mi = request.POST["min"]
            mx = request.POST["max"]
            print(excel_file,'fileeeeeeeeeeeeeee')
            data=pd.read_excel(excel_file)
            nums = [10.0,5.0,7.0,5.0,4.0,2.0,numpy.nan,7.0,9.0]
            index_col=[]
            for i in range(len(data)):
                index_col.append(i)
            data.insert(0,'index_abxyz',index_col)    
            data['random'] = nums
            print(data)
            data_copy = data.copy()
            def settings_view(data):
                # column_names = input('Column name: ').split(' ') #ip
                column_names.insert(0,'index_abxyz')
                print("jaiiiiiiiiiiiiii",column_names)
                col_dict = {'index_abxyz':['include',0,len(data)]} # brute force to neglect the errror
            #     col_dict={}
                dict_graph={}
                it=0
                data_len = len(data)
                enter_other=False
                enter_one = True
                key_idx=0
                col_idx=0
                highlighted,unhighlighted=0,0
                for i in range(len(column_names)):
                    if i ==0:
                        continue
                    if column_names[i] in data.columns:
                        allowed = str(inc)#2 values can be there include or exclude #ip
                        min_val = int(mi) #ip
                        max_val = int(mx) #ip
                        if min_val>max_val:
                            print('min value cannot be greater than max value')
                            return 0
                        records_list = [allowed,min_val,max_val]
                        col_dict.update({column_names[i]:records_list})
                    else:
                        print('Invalid column name check for typos')
                        return 0
                is_int=False
                is_string=False
                is_float=False
                print(column_names)
                print(col_dict)

                #Only to check if columns are  
                for column_name in column_names:
                    if type(data[column_name][0]) == numpy.int64:
                        print('its int')
                        try:
                            for i,each_value in enumerate(data[column_name]):
                                if type(each_value) == int:
                                    is_int=True
                                    continue

                                else:
                                    is_int=False
                                    print("The column chosen doesn't contain all int values, check for float, string or missing values")
                                    return 0
                        except:
                            print('ok')

                    if type(data[column_name][0]) == numpy.float64:
                        print('its float')
                        try:
                            for each_value in data[column_name]:
                                if type(each_value) == float:
                                    is_float=True
                                    continue
                                else:
                                    is_float=False
                                    print("The column chosen doesn't contain all float values, check for int, string or missing values")
                                    return 0
                        except:
                            print('float ok')


                    if type(data[column_name][0]) == str:
                        print('its string')
                        try:
                            for each_value in data[column_name]:
                                if type(each_value) == str:
                                    is_string=True
                                    continue
                                else:
                                    is_string=False
                                    print("The column chosen doesn't all string valus, check for float, int or missing values")
                                    return 0
                        except:
                            print('str ok')

                #this should be the last thing to be executed
                def color_negative_red(value):
                    nonlocal it,data_len,col_dict,enter_one,enter_other,enter_one,data,key_idx,dict_graph,highlighted,unhighlighted,col_idx,column_names
                    print(f'it  {it}  {value}')
                #     print('entered')
                    if enter_one:
                #         print(1)
                        if it == (data_len*2)-1:
                #             print(2)
                            print('pass')
                #             print(res)
                            data_len=data_len+(data_len*2)
                            print(data_len)
                            dict_graph.update({column_names[col_idx]:[round(highlighted/2),len(data)-round(highlighted/2)]}) #counts to make the graphs
                            col_idx+=1
                            highlighted,unhighlighted=0,0
                            enter_other=True
                            enter_one=False
                            key_idx+=1
                    elif enter_other:
                #         print(3)
                        if it == (data_len)-1:
                #             print(4)
                            print('pass two')
                            dict_graph.update({column_names[col_idx]:[highlighted,unhighlighted]}) #counts to make the graphs
                            col_idx+=1
                            highlighted,unhighlighted=0,0
                            data_len+=len(data)
                            print(data_len)
                            key_idx+=1
                    if key_idx!=len(col_dict):
                #         print(5)
                        res = list(col_dict.keys())[key_idx]
                #         print(res)
                        range_= col_dict[res][0]
                        min_value= col_dict[res][1]
                        max_value= col_dict[res][2]
                    else:
                        print(6)
                        # key_idx was increamented one extra time so need to apply this to get everything correct

                        res = list(col_dict.keys())[-1] # column wise keys
                        range_= col_dict[res][0]
                        min_value= col_dict[res][1]
                        max_value= col_dict[res][2]
                        entered=True


                #     print(value)
                    color='black'
                    if range_ == 'include': #if the setting is include then apply the below settings
                        if type(value) == int:
                            if value<=max_value and value>=min_value:
                                color = 'red'
                                highlighted+=1
                            else:
                                unhighlighted+=1


                        if type(value) == float:
                            if value<=max_value and value>=min_value:
                                color = 'red'
                                highlighted+=1
                            else:
                                unhighlighted+=1

                        if type(value) == str:
                            if len(value)<=max_value and len(value)>=min_value:
                                color='red'
                                highlighted+=1
                            else:
                                unhighlighted+=1
                    if range_ == 'exclude':# if value is not in range that means it is out of range so it is excluded
                        if type(value) == int:
                            if value not in range(min_value,max_value+1):
                                color = 'red'
                                highlighted+=1
                            else:
                                unhighlighted+=1

                        if type(value) == float:
                            if value not in range(min_value,max_value+1):
                                color = 'red'
                                highlighted+=1
                            else:
                                unhighlighted+=1

                        if type(value) == str:
                            if len(value) not in range(min_value,max_value+1):
                                color='red'
                                highlighted+=1
                            else:
                                unhighlighted+=1

                    it+=1
                    try:
                        if entered:
                            total_highlighted = 0
                            total_unhighlighted = 0
                            for v in dict_graph.values():
                                total_highlighted+=v[0]
                                total_unhighlighted+=v[1]
                    #         print(f'{total_highlighted}  {total_unhighlighted}')
                            dict_graph.update({'total_highlighted':total_highlighted})
                            dict_graph.update({'total_unhighlighted':total_unhighlighted})
                            for k in dict_graph:
                                dict_graph[k] -= 1
                    except:
                        pass


                    return 'color: %s' % color

                data_copy = data.style.applymap(color_negative_red,subset = column_names)
                data_copy.hide_columns(subset='index_abxyz')# this is bruteforce column we don't want to see it
                return data_copy,dict_graph
            data_copy,dict_graph = settings_view(data)
            # print(data_copy)

            return HttpResponse(data_copy.render())
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




