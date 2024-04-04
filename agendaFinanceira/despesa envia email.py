from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def cadastrar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            # Associate the logged-in user with the 'usuario' field before saving
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            
            # Send an email alert to the admin user
            subject = 'New Despesa Alert'
            message = 'A new despesa has been added: {}'.format(despesa)
            from_email = 'your_email@example.com'  # Update with your email
            recipient_list = [request.user.email]  # Use the admin user's email
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            messages.success(request, 'Despesa cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Despesa. Verifique os campos.')
    else:
        form = DespesaForm()

    return render(request, 'agendaFinanceiraApp/cadastroDespesa.html', {'form': form})
