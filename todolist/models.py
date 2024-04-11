from django.db import models
from usuarios.models import User
# Create your models here.
from django.conf import settings
from django.utils import timezone
import datetime

class todolist(models.Model):
	title = models.CharField(max_length=40, verbose_name="Titulo")
	description = models.TextField(blank = True, verbose_name="Descrição")
	created = models.DateTimeField(auto_now = True)
	datecompleted = models.DateTimeField(null=True,blank = True, verbose_name="Conclusão da Atividade")
	priority = models.BooleanField(default=False, verbose_name="Prioridade")
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	date_conclusao = models.DateTimeField(default=timezone.now, verbose_name="Data da Atividade")

	def __str__(self):
		return self.title
