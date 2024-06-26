# Generated by Django 3.2.9 on 2024-04-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendaFinanceira', '0006_auto_20240402_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cnpj_cpf',
            field=models.CharField(max_length=18, unique=True, verbose_name='PIX_CPF'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='PIX_Email'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=20, verbose_name='PIX_Telefone'),
        ),
    ]
