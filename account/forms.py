from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'full_name', 'password1', 'password2', 'role')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'full_name')