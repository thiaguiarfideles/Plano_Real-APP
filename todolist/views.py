from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from usuarios.models import User
from django.db import IntegrityError
from django.utils import timezone
from todolist.forms import TodoForm
from todolist.models import todolist

# Create your views here.
def hometodo(request):
	return render(request,'home_todo.html')


def createtodolist(request):
	if request.method == 'GET':
		return render(request,'todolist/createtodolist.html',{'form':TodoForm()})
	else:
		try:
			todos = TodoForm(request.POST)
			new_todo = todos.save(commit=False)
			new_todo.user = request.user
			new_todo.save()
			return redirect('currenttodolist')
		except ValueError:
			return render(request,'todolist/createtodolist.html',{'form':TodoForm(),'error':'Bad Value'})


def currenttodolist(request):
	todos = todolist.objects.filter(user=request.user,datecompleted__isnull=True)
	return render(request,'todolist/currentlist.html',{'todos':todos})


def displaytodolist(request, todolist_pk):
	todos = get_object_or_404(todolist ,pk=todolist_pk, user=request.user)
	if request.method =='GET':
		form = TodoForm(instance=todos)
		return render(request,'todolist/displaytodo.html',{'form':form, 'todos':todos})
	else:
		try:
			form = TodoForm(request.POST,instance=todos)
			form.save()
			return redirect('currenttodolist')
		except:
			return render(request,'todolist/displaytodo.html',{'form':TodoForm(),'error':'Bad value passed in','todos': todos})


def completedtodolist(request):
	todos = todolist.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
	return render(request,'todolist/completedlist.html',{'todos': todos})



def completetodolist(request, todolist_pk): 
    todo = get_object_or_404(todolist, pk=todolist_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodolist')


def deletetodolist(request, todolist_pk):
    todo = get_object_or_404(todolist, pk=todolist_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodolist')
