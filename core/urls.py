"""controle_hc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.conf.urls import url
from django.urls import path,include, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views import static as ds

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core.views import LoginView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    #path('usuarios/create_user', CreateUserView.as_view(), name='create_user'),
    path('usuarios/',include('usuarios.urls')),
    path('', views.home1, name='home1'),
    path('todolist/',include('todolist.urls')),
    path('agendaFinanceira/',include('agendaFinanceira.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # URL para obter um token de autenticação


    re_path(r'^prestador/', include(('usuarios.urls', 'usuarios'),namespace='usuarios')),
    re_path(r'^prestador/', include(('prestadores.urls','prestadores'),namespace='prestadores')),
    re_path(r'^select2/', include('django_select2.urls')),
     

    re_path(r'^media/(?P<path>.*)$', ds.serve,
            {'document_root': settings.MEDIA_ROOT, }, name="media"),
] 
urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
