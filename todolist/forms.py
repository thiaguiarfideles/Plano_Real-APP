from django.forms import ModelForm
from .models import todolist

class TodoForm(ModelForm):

	class Meta:
		model =  todolist
		exclude=['user']
		fields = ['title','description','priority', 'date_conclusao',]