from django import forms
from .models import SubscribedUsers

class SubscribeUserForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['email']