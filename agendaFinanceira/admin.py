from django.contrib import admin
from .models import *

admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(SaldoInicial)
admin.site.register(OrcamentoGastos)
admin.site.register(OrcamentoReceitas)
admin.site.register(Receita)
admin.site.register(Despesa)
admin.site.register(Gasto)
admin.site.register(LancamentoContasPagar)
admin.site.register(LancamentoContasReceber)
