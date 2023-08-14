from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from mafia.models.gangster import Gangster
from .models.gangster import Gangster
from mafia.middlewares.auth import auth_middleware

# Create your views here.

@auth_middleware
def Khoj(request):
    return render(request, 'home.html')

@auth_middleware
def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None;
        gangster = Gangster(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        if (not gangster.first_name):
            error_message = "First Name Required !!"
        elif len(gangster.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not gangster.last_name:
            error_message = 'Last Name Required'
        elif len(gangster.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not gangster.phone:
            error_message = 'Phone Number required'
        elif len(gangster.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(gangster.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(gangster.email) < 5:
            error_message = 'Email must be 5 char long'
        elif gangster.isExists():
            error_message = 'Email Address Already Registered..'

        # save
        if not error_message:
            print(first_name, last_name, phone, email, password)
            gangster.password = make_password(gangster.password)
            gangster.register()
            return redirect('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


def LoginPage(request):
    if request.method == 'GET':
       return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        gangster = Gangster.get_gangster_by_email(email)
        error_message = None
        if gangster:
            flag = check_password(password, gangster.password)
            if flag:
                request.session['gangster'] = gangster.id
                return redirect('home')

            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

