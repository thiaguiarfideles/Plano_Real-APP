import datetime 
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
#from isoduration import format_duration
from agendaFinanceira import models
from usuarios.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from agendaFinanceira.models import Cliente, Fornecedor, LancamentoContasPagar, Receita, Despesa, SaldoAtual,Cliente, Produto
from .models import Cliente, Fornecedor, LancamentoContasPagar, Receita, Despesa, SaldoAtual,Produto


from agendaFinanceira.forms import ( ClienteForm, FornecedorForm, ReceitaForm, DespesaForm, LancamentoContasPagarForm, SaldoAtlForm, SaldoForm, ProdutoForm)
from .serializers import DespesaSerializer, ReceitaSerializer, ClienteSerializer
from .utils import get_financial_data
from dal import autocomplete
import logging
from django.db.models import Sum,Func, Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import F, ExpressionWrapper, DecimalField
from agendaFinanceira.filters import register
import pandas as pd
import pickle
import datetime




# Create your views here.

# Pagina inicial
def index(request):
	return render(request, 'agendaFinanceira/index.html', {})

# Cadastrar Usuario

# Logout
def sair(request):
	logout(request)
	return redirect('/')

# -----views com obrigatoriedade de login-----
	
# Menu inical apos login
@login_required
def menu(request):
	return render(request, 'agendaFinanceira/menu.html', {})



@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.save()
            # Obter o produto selecionado no formulário
            produto_id = request.POST.get('produto')
            if produto_id:
                # Associar o produto à receita
                receita.produto_id = produto_id
                receita.save()
            messages.success(request, 'Receita cadastrada com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Receita. Verifique os campos.')
    else:
        form = ReceitaForm()

    return render(request, 'agendaFinanceiraApp/cadastroReceita.html', {'form': form})

@login_required
def excluir_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    if receita.usuario == request.user:
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para excluir esta receita.')
    return redirect('home')

# Visualização para detalhar, atualizar e excluir receitas
#class ReceitaDetailView(generics.RetrieveUpdateDestroyAPIView):
    #queryset = Receita.objects.all()
    #serializer_class = ReceitaSerializer
    

class FornecedorAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Seu código para obter a lista de fornecedores aqui
        queryset = Fornecedor.objects.all()

        if self.q:
            queryset = queryset.filter(nome__icontains=self.q)

        return queryset


@login_required  # Ensure that the user is logged in to access this view
def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            # Associate the logged-in user with the 'usuario' field before saving
            fornecedor = form.save(commit=False)
            fornecedor.usuario = request.user  # Assign the logged-in user to the 'usuario' field
            fornecedor.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Fornecedor. Verifique os campos.')
    else:
        form = FornecedorForm()

    return render(request, 'agendaFinanceiraApp/cadastroFornecedor.html', {'form': form})

def cadastrar_contasapagar(request):
    if request.method == 'POST':
        form = LancamentoContasPagarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contas a pagar cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Contas a pagar. Verifique os campos.')
    else:
        form = LancamentoContasPagarForm()

    return render(request, 'agendaFinanceiraApp/lancamento_fornecedor.html', {'form': form})


# Visualização para listar e criar despesas
@login_required  # Ensure that the user is logged in to access this view
def cadastrar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            # Associate the logged-in user with the 'usuario' field before saving
            despesa = form.save(commit=False)
            despesa.usuario = request.user  # Assign the logged-in user to the 'usuario' field
            despesa.save()
            messages.success(request, 'Despesa cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Despesa. Verifique os campos.')
    else:
        form = DespesaForm()

    return render(request, 'agendaFinanceiraApp/cadastroDespesa.html', {'form': form})

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os campos.')
    else:
        form = ClienteForm()

    return render(request, 'agendaFinanceiraApp/cadastroCliente.html', {'form': form})

@login_required  # Ensure that the user is logged in to access this view
def saldoinicial(request):
    if request.method == 'POST':
        form = SaldoForm(request.POST)
        if form.is_valid():
            # Associate the logged-in user with the 'usuario' field before saving
            saldo = form.save(commit=False)
            saldo.usuario = request.user  # Assign the logged-in user to the 'usuario' field
            saldo.save()
            messages.success(request, 'Saldo Inicial cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Saldo Inicial. Verifique os campos.')
    else:
        form = SaldoForm()

    return render(request, 'agendaFinanceiraApp/cadastroSaldoinicial.html', {'form': form})


@login_required  # Ensure that the user is logged in to access this view
def saldoatual(request):
    if request.method == 'POST':
        form = SaldoAtlForm(request.POST)
        if form.is_valid():
            # Associate the logged-in user with the 'usuario' field before saving
            atual = form.save(commit=False)
            atual.usuario = request.user  # Assign the logged-in user to the 'usuario' field
            atual.save()
            messages.success(request, 'Saldo Atual cadastrado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao cadastrar Saldo Atual. Verifique os campos.')
    else:
        form = SaldoAtlForm()

    return render(request, 'agendaFinanceiraApp/cadastroSaldoatual.html', {'form': form})

from datetime import datetime

@login_required
def update_saldo_atual(request, pk):
    saldoatual = get_object_or_404(SaldoAtual, pk=pk)
    
    if request.method == 'POST':
        form = SaldoAtlForm(request.POST, instance=saldoatual)
        if form.is_valid():
            # Set the date_modificacao field to the current date and time
            saldoatual.date_modificacao = datetime.now()
            form.save()
            return redirect('saldoatual')
    else:
        form = SaldoAtlForm(instance=saldoatual)
    
    return render(request, 'agendaFinanceiraApp/update_saldo_atual.html', {'form': form, 'saldoatual': saldoatual})


class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cliente.objects.all()

        if self.q:
            qs = qs.filter(nm_cliente__icontains=self.q)

        return qs

    

class ClienteListView(ListView):
    model = Cliente
    queryset = Cliente.objects.order_by('nm_cliente')  # Substitua 'your_field' pelo campo pelo qual deseja ordenar
    template_name = 'dashboard.html'  # Substitua 'your_template.html' pelo seu template
    context_object_name = 'clientes'
    paginate_by = 10

@login_required
def cliente_list(request):
    usuario = request.user
    cadastros = Cliente.objects.filter(usuario=usuario.id)
    return render(request, 'cliente_list.html', {
        'cadastros': cadastros
    })

@login_required
def fornecedor_list(request):
    usuario = request.user
    cadastros = Fornecedor.objects.filter(usuario=usuario.id)
    return render(request, 'fornecedor_list.html', {
        'cadastros': cadastros
    })


@login_required    
def despesa_list(request):
    usuario = request.user
    cadastros = Despesa.objects.filter(usuario=usuario.id)
    return render(request, 'despesa_list.html', {
        'cadastros': cadastros
    })        



@login_required
def receitas_list(request):
    usuario = request.user
    receitas = Receita.objects.filter(usuario=usuario.id)
    total_valor = receitas.aggregate(Sum('valor'))['valor__sum']
    # Log dos dados retornados
    logging.info(f'Dados das receitas retornadas: {receitas}')
    

    # Imprimir as informações no console
    for receita in receitas:
        print(f'Cliente: {receita.cliente.nm_cliente}')
        print(f'Valor: {receita.valor}')
        print(f'Data Entrada: {receita.data_entrada}')
        print(f'Forma de Recebimento: {receita.forma_recebimento}')
        print(f'Situação: {receita.situacao}')
        print(f'Observações: {receita.observacoes}')

    return render(request, 'agendaFinanceiraApp/consultaReceita.html', {
        'receitas': receitas,
        'total_valor': total_valor
    })



@login_required        
def saldoatual_list(request):
    usuario = request.user
    cadastros = SaldoAtual.objects.filter(usuario=usuario.id)
    
    for cadastro in cadastros:
        # Calculate the difference between date_modificacao and created_at
        cadastro.date_diff = cadastro.date_modificacao - cadastro.created_at
        # Calculate days, hours, and minutes
        days, seconds = cadastro.date_diff.days, cadastro.date_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        # Format the duration
        cadastro.formatted_date_diff = f"{days} days, {hours} hours, {minutes} minutes"

    return render(request, 'saldoatual_list.html', {'cadastros': cadastros})
    


@login_required
class ListarLancamentosView(ListView):
    model = LancamentoContasPagar
    template_name = 'view_apagar.html'
    context_object_name = 'lancamentos'
    
    
class Strftime(Func):
    function = 'STRFTIME'
    template = "%(function)s('%Y-%m', %(expressions)s)"

@login_required
def dashboard(request):
    usuario = request.user

    # Exemplo de consulta para obter o total recebido de cada cliente
    total_por_cliente = Receita.objects.filter(usuario=usuario.id).values('cliente__nm_cliente').annotate(total=Sum('valor'))

    # Exemplo de consulta para obter o total pago por período
    total_por_periodo = Receita.objects.filter(usuario=usuario.id).values('cliente__nm_cliente') \
    .annotate(
        ano=ExtractYear('data_entrada'),
        mes=ExtractMonth('data_entrada')
    ) \
    .values('ano', 'mes') \
    .annotate(total=Sum('valor'))
    
    

    context = {
        'total_por_cliente': total_por_cliente,
        'total_por_periodo': total_por_periodo
    }

    return render(request, 'agendaFinanceiraApp/dashboard.html', context)

@login_required
@register.filter
def dashboard_produto(request):
    usuario = request.user
    produtos = Produto.objects.filter(usuario=usuario)
    
    # Consulta para contar a quantidade de produtos
    total_produtos = produtos.count()
    
    # Consulta para obter a contagem de vendas por produto
    vendas_por_produto = produtos.annotate(total_vendas=Count('receita')).order_by('-total_vendas')[:5]
    
    # Calcular o total de produtos vendidos para cada produto
    total_produtos_vendidos = []
    for produto in produtos:
        total_vendido_produto = Receita.objects.filter(produto=produto).aggregate(total=Sum('quantidade'))['total']
        total_produtos_vendidos.append(total_vendido_produto or 0)
    
    # Preparar dados para o gráfico de barras radiais
    categorias = [produto.nm_produto for produto in vendas_por_produto]
    total_vendas = [produto.total_vendas for produto in vendas_por_produto]
    
    context = {
        'produtos': produtos,
        'total_produtos': total_produtos,
        'vendas_por_produto': vendas_por_produto,
        'categorias': categorias,
        'total_vendas': total_vendas,
        'total_produtos_vendidos': total_produtos_vendidos,  # <-- Passa a quantidade de produtos vendidos para o template
    }
    
    return render(request, 'agendaFinanceiraApp/dashboard_produto.html', context)






class ProdutoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Produto.objects.all()

        if self.q:
            qs = qs.filter(nm_produto__icontains=self.q)

        return qs

@login_required
def listar_produtos(request):
    produtos = Produto.objects.filter(usuario=request.user)
    return render(request, 'agendaFinanceiraApp/listar_produtos.html', {'produtos': produtos})


@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.usuario = request.user
            produto.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'agendaFinanceiraApp/cadastrar_produto.html', {'form': form})

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'agendaFinanceiraApp/editar_produto.html', {'form': form})

def excluir_produto(request, id_produto):
    produto = get_object_or_404(Produto, id_produto=id_produto)
    produto.delete()
    return redirect('agendaFinanceiraApp/listar_produtos')



def todas_as_paginas(request):
    return render(request, 'agendaFinanceiraApp/todas_as_paginas.html')


# Carregue o modelo treinado
with open('financial_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Função para obter dados financeiros (esta pode ser a mesma do script de treinamento)
def get_financial_data():
    # Obter as receitas do banco de dados
    receitas_queryset = Receita.objects.all().values(
        'data_entrada', 'quantidade', 'valor', 'cliente__nm_cliente', 'forma_recebimento', 'situacao', 'observacoes'
    )
    df_receitas = pd.DataFrame(receitas_queryset)
    print("DataFrame Receitas original:")
    print(df_receitas.head())
    
    df_receitas.rename(columns={'data_entrada': 'data', 'quantidade': 'quantidade_receita', 'valor': 'valor_receita'}, inplace=True)
    print("DataFrame Receitas após renomear colunas:")
    print(df_receitas.head())
    
    # Obter as despesas do banco de dados
    despesas_queryset = Despesa.objects.all().values(
        'data_vencimento', 'valor', 'nome_credor__nm_fornecedor', 'situacao', 'observacoes', 'tipo_despesa', 'modo_pag'
    )
    df_despesas = pd.DataFrame(despesas_queryset)
    print("DataFrame Despesas original:")
    print(df_despesas.head())
    
    if not df_despesas.empty:
        df_despesas.rename(columns={'data_vencimento': 'data', 'valor': 'valor_despesa'}, inplace=True)
        df_despesas['quantidade_despesa'] = 1  # Adicionar coluna quantidade_despesa com valor padrão
    else:
        # Adiciona colunas necessárias com valores padrão se não houver despesas
        df_despesas['data'] = []
        df_despesas['valor_despesa'] = []
        df_despesas['quantidade_despesa'] = []
        
    print("DataFrame Despesas após renomear colunas:")
    print(df_despesas.head())

    return df_receitas, df_despesas

@login_required
def get_financial_data_view(request):
    df_receitas, df_despesas = get_financial_data()

    # Verificar se as colunas 'data' estão presentes
    if 'data' not in df_receitas.columns:
        raise KeyError("'data' column is missing in df_receitas")
    if 'data' not in df_despesas.columns:
        raise KeyError("'data' column is missing in df_despesas")
    
    # Mesclar DataFrames de receitas e despesas com base na coluna 'data'
    df = pd.merge(df_receitas, df_despesas, on="data", how="outer").fillna(0)
    
    # Verificar se a coluna 'data' está presente após a mesclagem
    if 'data' not in df.columns:
        raise KeyError("'data' column is missing after merging df_receitas and df_despesas")
    
    # Verificar se as colunas necessárias estão presentes e preencher valores nulos
    required_columns = ['quantidade_receita', 'valor_receita', 'quantidade_despesa', 'valor_despesa']
    for column in required_columns:
        if column not in df.columns:
            df[column] = 0
        else:
            df[column] = df[column].fillna(0)
    
    # Selecionar as colunas para X
    X = df[['quantidade_receita', 'valor_receita', 'quantidade_despesa', 'valor_despesa']]
    
    # Faça previsões usando o modelo
    y = model.predict(X)
    
    # Transformar os dados para renderizar no template
    X = X.to_dict(orient='records')
    y = y.tolist()

    # Adicionar prints para depuração
    print("Dados de Entrada (X):", X)
    print("Resultados Previstos (y):", y)

    context = {
        'X': X,
        'y': y
    }

    return render(request, 'agendaFinanceiraApp/financial_data.html', context)

