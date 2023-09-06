from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm, UserChangeForm

from django.contrib.auth.models import Group, User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


'''class PasswordChangingForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New password'}))
    class Meta:
        model = User
        fields = ['new_password1','new_password2']'''


class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = '__all__'
