from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите эл.почту'

        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите эл.почту'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class UserProfileForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "readonly": True,
            }
        )
    )
    age = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control py-4",
                "readonly": True,
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
            }
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={"class": "custom-file-label"},
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image",
                  "username", "email", "age")
