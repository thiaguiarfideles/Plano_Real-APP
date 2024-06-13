from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from .models import todolist
from .forms import TodoForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def hometodo(request):
	return render(request,'todolist/home_todo.html')


@login_required
def createtodolist(request):
    if request.method == 'GET':
        return render(request, 'todolist/createtodolist.html', {'form': TodoForm()})
    else:
        try:
            todos = TodoForm(request.POST)
            new_todo = todos.save(commit=False)  # Não salva imediatamente
            new_todo.user = request.user
            new_todo.save()  # Salva após definir o usuário
            return redirect('currenttodolist')
        except ValueError:
            return render(request, 'todolist/createtodolist.html', {'form': TodoForm(), 'error': 'Sem valores'})


@login_required
def currenttodolist(request):
    todos = todolist.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todolist/currentlist.html', {'todos': todos})


@login_required
def displaytodolist(request, todolist_pk):
    todos = get_object_or_404(todolist, pk=todolist_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todos)
        return render(request, 'todolist/displaytodo.html', {'form': form, 'todos': todos})
    else:
        try:
            form = TodoForm(request.POST, instance=todos)
            if form.is_valid():
                updated_todo = form.save(commit=False)
                logger.info("Form save successful: %s", updated_todo)

                # Captura o email do formulário
                email_to = form.cleaned_data.get('email')
                logger.info("Email provided in form: %s", email_to)
                print('Email formulario', email_to)

                # Atualizar o campo de email no modelo
                updated_todo.email = email_to

                # Verifique se o e-mail foi atualizado e se é válido
                if email_to:
                    logger.info("Email update detected: %s", email_to)

                    # Renderize o template do email
                    email_html_message = render_to_string('email_templates/redirected_activity_email.html', {
                        'title': updated_todo.title,
                        'postpone_date': updated_todo.postpone_date,
                        'description': updated_todo.description,
                    })

                    # Envie o e-mail
                    try:
                        email = EmailMultiAlternatives(
                            subject='Atividade Redirecionada',
                            body=email_html_message,
                            from_email='seumkt@gmail.com',
                            to=[email_to],
                        )
                        
                        email.attach_alternative(email_html_message, "text/html")
                        email.send()
                        logger.info("Email enviado com sucesso para: %s", email_to)
                    except Exception as e:
                        logger.error("Erro ao enviar o email: %s", e)
                        print('Email enviado', email_to)
                        print('Email erro', e)

                # Envie e-mail para o usuário original (opcional)
                original_user_email = todos.user.email
                if original_user_email:
                    try:
                        email_html_message = render_to_string('email_templates/updated_activity_email.html', {
                            'title': updated_todo.title,
                            'postpone_date': updated_todo.postpone_date,
                            'description': updated_todo.description,
                        })
                        email = EmailMultiAlternatives(
                            subject='Atualização da Atividade',
                            body=email_html_message,
                            from_email='seumkt@gmail.com',
                            to=[original_user_email],
                        )
                        email.attach_alternative(email_html_message, "text/html")
                        email.send()
                        logger.info("Email enviado com sucesso para o usuário original: %s", original_user_email)
                    except Exception as e:
                        logger.error("Erro ao enviar o email para o usuário original: %s", e)
                
                updated_todo.save()
                return redirect('currenttodolist')
            else:
                logger.error("Formulário inválido: %s", form.errors)
        except ValueError as e:
            logger.error("Erro de valor: %s", e)
            return render(request, 'todolist/displaytodo.html', {'form': form, 'error': 'Bad value passed in', 'todos': todos})

@login_required
def completetodolist(request, todolist_pk):
    todo = get_object_or_404(todolist, pk=todolist_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodolist')
    return redirect('currenttodolist')  # Certifique-se de sempre retornar uma resposta HTTP

@login_required
def completedtodolist(request):
    todos = todolist.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todolist/completedlist.html', {'todos': todos})


def deletetodolist(request, todolist_pk):
    todo = get_object_or_404(todolist, pk=todolist_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodolist')
