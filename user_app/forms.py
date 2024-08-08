from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm

from config.forms import StyleFormMixin
from user_app.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'email')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'open_email', 'country', 'about')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserResetPasswordForm(StyleFormMixin, PasswordResetForm):
    pass


class UserPasswordResetConfirmForm(StyleFormMixin, SetPasswordForm):
    pass

