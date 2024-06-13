from django.db import models
from usuarios.models import User
from django.conf import settings
from django.utils import timezone

class todolist(models.Model):
    title = models.CharField(max_length=40, verbose_name="Titulo")
    description = models.TextField(blank=True, verbose_name="Descrição")
    created = models.DateTimeField(auto_now=True)
    datecompleted = models.DateTimeField(null=True, blank=True, verbose_name="Conclusão da Atividade")
    priority = models.BooleanField(default=False, verbose_name="Prioridade")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_todolist")
    date_conclusao = models.DateTimeField(default=timezone.now, verbose_name="Data da Atividade")
    is_completed = models.BooleanField(default=False, verbose_name="Atividade Realizada")
    postpone_date = models.DateTimeField(null=True, blank=True, verbose_name="Postergar Data")
    email = models.EmailField(blank=True, null=True, verbose_name="Email para Redirecionamento")
    redirected_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="redirected_todolist")

    def __str__(self):
        return self.title
