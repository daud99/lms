from django.shortcuts import render, redirect
from django.contrib import messages, auth
from account.models import User, UserRole
# Create your views here.

def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('/signup')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        full_name = request.POST['full_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is taken')
                return redirect('signup')
            else:

                if UserRole.objects.filter(role_name=role).exists():
                    user_role = UserRole.objects.get(role_name=role)
                    user = User.objects.create_user(email=email, password=password, full_name=full_name, role=user_role)
                    user.save()
                    messages.success(request, 'You are now successfully register and log in')
                    return redirect('login')
                else:
                    messages.error(request, 'Invalid role')
                    return redirect('signup')


        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

    else:

        return render(request, 'registration/signup.html')


