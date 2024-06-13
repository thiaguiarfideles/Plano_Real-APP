from django import forms
from .models import todolist

class TodoForm(forms.ModelForm):
    class Meta:
        model = todolist
        exclude = ['user', 'date_conclusao']
        fields = ['title', 'description', 'datecompleted', 'priority', 'email', 'postpone_date', 'redirected_user']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'priority': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'postpone_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email para Redirecionamento'}),
        }