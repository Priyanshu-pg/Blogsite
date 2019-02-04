from django import forms
from .models import SubscribedUsers

class SubscribeUserForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={
                'id': 'email-text',
                'required': True,
                'placeholder': 'Enter your email'
            }),
        }

class ConfirmSubscriberForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['frequency', 'tags_followed']