from django.urls import path,include, re_path
from . import views
from django.views import static as ds
from django.conf import settings
from django.conf.urls.static import static
from .views import create_user,editar_perfil,perfil

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('perfil', views.perfil, name="perfil_usuario"),
    path('perfil/editar', views.editar_perfil,name="editar_perfil"),

    re_path(r'^media/(?P<path>.*)$', ds.serve,
            {'document_root': settings.MEDIA_ROOT, }, name="media"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)