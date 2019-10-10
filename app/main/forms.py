from django import forms
from .models import Text


class TextModelForm(forms.ModelForm):
    title = forms.CharField(label='Tytuł',
                            min_length=3,
                            max_length=200)

    content = forms.CharField(label='Tekst',
                              min_length=3,
                              widget=forms.Textarea(attrs={'rows': 10}))

    class Meta:
        model = Text
        fields = ['title', 'content']
