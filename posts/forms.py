from django import forms
from .models import SubscribedUsers

class SubscribeUserForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['email']

class ConfirmSubscriberForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['frequency', 'tags_followed']