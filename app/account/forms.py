from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1',
                  'password2', 'is_writer']


class UpdateUserForm(ModelForm):
    # password = None

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']
        exclude = ['password1', 'password2']
