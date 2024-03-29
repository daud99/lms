from django.shortcuts import render, redirect
from django.contrib import messages, auth
from account.models import User, UserRole
from event.forms import LocationForm
from account.forms import CustomUserCreationForm
from LMS import common

# Create your views here.

def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

@login_excluded("dashboard:index")
def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, user_password=password)
            if user is not None:
                common.downloadImageFromFTP(user.image_url)
                auth.login(request, user)
                return redirect('dashboard:index')
            else:
                messages.error(request, 'Invalid Credentials')
                context = {"values": request.POST}
                return render(request, 'registration/login.html', context=context)
        except Exception as e:
            print("exception while loging in no user found")
            print(e)
            messages.error(request, "The user with this email doesn't exist")
            context = {"values": request.POST}
            return render(request, 'registration/login.html', context=context)
    else:
        return render(request, 'registration/login.html')

@login_excluded("dashboard:index")
def signup(request):
    if request.method == "POST":
        location = {}
        if "location" in request.POST:
            location = common.processLocation(request.POST["location"])
        print("location is")
        print(location)
        email = request.POST['email']
        full_name = request.POST['full_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        role = request.POST['role']
        image = request.FILES['image']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already taken')
                form = LocationForm()
                context = {"values": request.POST, "form": form}
                return render(request, 'registration/signup.html', context=context)
            else:

                if UserRole.objects.filter(role_name=role).exists():
                    common.uploadImageToFTP(image.name, image)
                    user_role = UserRole.objects.get(role_name=role)
                    user = User(email=email, user_password=password, full_name=full_name, role=user_role, image_url=image.name, location=location)
                    user.save()
                    messages.success(request, 'You are now successfully register and log in')
                    return redirect('account_login')
                else:
                    form = LocationForm()
                    messages.error(request, 'Invalid role')
                    context = {"values": request.POST, "form": form}
                    return render(request, 'registration/signup.html', context=context)


        else:
            form = LocationForm()
            messages.error(request, 'Passwords do not match')
            context = {"values": request.POST, "form": form}
            return render(request, 'registration/signup.html', context=context)

    else:
        form = LocationForm()
        context = {
            "form": form
        }
        return render(request, 'registration/signup.html', context)
