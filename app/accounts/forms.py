from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label='Motto',
                          widget=forms.Textarea(attrs={'rows': 3}))

    location = forms.CharField(label='Lokalizacja',
                               max_length=200)

    class Meta:
        model = Profile
        fields = ('bio', 'location',)
