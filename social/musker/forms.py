from django import forms
from .models import Meep, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
        attrs={
            "placeholder": "Comment...",
            "class": "form-control"
            }),
        label=''
    )

    class Meta:
        model = Comment
        exclude = ('user', 'meep')

class MeepForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter your Meep!",
                "class": "form-control",
                }),
        label='',
    )
    meep_image_url = forms.ImageField(required=False, label='')

    class Meta:
        model = Meep
        exclude = ('user', 'likes', )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="first name", max_length=40, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="last name", max_length=40, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Username'})
        self.fields['username'].label = "username"

        self.fields['password1'].widget.attrs.update({'class':'form-control', 'placeholder':'Password'})
        self.fields['password1'].label = "pass1"

        self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Password'})
        self.fields['password2'].label = "pass2"


class ProfilePictureForm(forms.ModelForm):
    profile_image_url = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('profile_image_url', )