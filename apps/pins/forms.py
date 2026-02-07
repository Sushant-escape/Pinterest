from django import forms
from .models import Pin
from apps.boards.models import Board

class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['title', 'description', 'image', 'link', 'board']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add your title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell everyone what your Pin is about', 'rows': 3}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Add a destination link'}),
            'board': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['board'].queryset = Board.objects.filter(user=user)
