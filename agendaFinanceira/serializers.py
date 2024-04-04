from rest_framework import serializers
from agendaFinanceira.models import *
from usuarios.models import User



class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = '__all__'  # Isso incluirá todos os campos do modelo 'Despesa'




class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = '__all__'
        

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'        
        
        
  
