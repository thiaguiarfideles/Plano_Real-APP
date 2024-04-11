from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
User = settings.AUTH_USER_MODEL




def login(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return redirect('home')
    return render(request, 'registration/login.html', {'selecteduser': user})        

def home(request):
    return render(request, template_name='home/home.html')

def home1(request):
    return render(request, 'core/home1.html')    


  



