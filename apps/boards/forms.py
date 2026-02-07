from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Board Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What is this board about?', 'rows': 3}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
