from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib import messages, auth
from accounts.models import Account
from django.contrib.auth import authenticate
# verify account


# Create your views here.


def register(request):
    if request.user.is_authenticated:
        response = redirect('index')
        response.set_cookie('user_id', request.user.id)
        return response
    if request.method == "POST":
        updated_request = request.POST.copy()
        updated_request.update({'username': request.POST['email']})
        form = RegistrationForm(updated_request)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phone_number = form.cleaned_data["phone_number"]
            username = form.cleaned_data["username"].split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username
            )
            user.phone_number = phone_number
            user.is_active = True
            user.save()
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        response = redirect('index')
        return response
    if request.method == "POST":
        print('checking form')
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            print(user)
            auth.login(request, user)
            messages.success(request, 'Welcome ' + request.user.username+'!')
            response = redirect('index')
            return response
        else:
            messages.warning(
                request, 'Invaldi username or password is incorrect!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged Out!')
    return redirect('login')
