from django import forms

from .models import *

class PostForm(forms.ModelForm):
    body = forms.CharField(max_length=256, 
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "post something here..."
            }
        ),
        label=""
    )
    class Meta:
        model = Post
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'password']

    