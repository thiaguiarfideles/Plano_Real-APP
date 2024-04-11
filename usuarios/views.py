from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import User, UserProfile
from django.contrib.auth import authenticate, login
from .forms import UserProfileForm,CustomUserCreationForm
from django.shortcuts import redirect

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # ou para qualquer outra página
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/create_user.html', {'form': form})

@login_required
def perfil(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return redirect('home')
    return render(request, 'usuarios/perfil.html', {'selecteduser': user})

@login_required
def editar_perfil(request):
    userprofile = UserProfile.objects.get(user=request.user.id)
    data = {'nm_completo': userprofile.nm_completo, 'nr_cpf_cgc': userprofile.nr_cpf_cgc,'foto_perfil':userprofile.foto_perfil}
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES,instance=userprofile)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
    else:
        form = UserProfileForm(initial=data)
    return render(request, 'usuarios/editar_perfil.html', {
        'form': form
    })
