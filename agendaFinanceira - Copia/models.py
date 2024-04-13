import os
from django.db import models
from django.utils.timezone import now as timezone_now
from usuarios.models import User
from django.utils import timezone
from core.helpers import validate_file_extension


def upload_to_despesa(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.id_despesa, "id_despesa_"+filename)

# Constants for choices
STATUS_RECEITA = (
    ('SALARIO', 'Salário'),
    ('REEMBOLSO', 'Reembolso'),
    ('FONTES_EXTERNAS', 'Fontes Externas'),
    ('OUTROS', 'Outros'),
)

STATUS_PAGAMENTO = (
    ('CONTAS', 'Contas'),
    ('COMPRAS_MERCADO', 'Compras Mercado'),
    ('COMPRAS_HORTIFRUTI', 'Compras Hortifruti'),
    ('COMPRAS_RESTAURANTE', 'Compras Restaurante'),
    ('COMPRAS_GERAL', 'Compras geral'),
    ('COMBUSTIVEL', 'Combustível'),
    ('ALUGUEL', 'Aluguel'),
    ('TV_INTERNET', 'TV/Internet'),
    ('TELEFONE', 'Telefone'),
    ('CARRO', 'Carro'),
    ('SEGURO', 'Seguro'),
    ('AGUA', 'Água'),
    ('LUZ', 'Luz'),
    ('CARTAO_CREDITO', 'Cartão de Crédito'),
    ('OUTROS', 'Outros'),
)

TIPO_PAGAMENTO = (
    ('CARTAO_CREDITO', 'Cartão de Crédito'),
    ('DINHEIRO', 'Dinheiro'),
    ('PIX', 'Pix'),
)

# Define choices for the income type field
TIPO_RECEITA = (
    ('RECEITA_PRODUTOS', 'Receita com Produtos'),
    ('RECEITA_SERVICOS', 'Receita com Serviços'),
    ('OUTRAS_RECEITAS', 'Outras Receitas'),
)

# Define choices for the expense type field
TIPO_GASTO = (
    ('CUSTOS_VARIAVEIS', 'Custos Variáveis'),
    ('CUSTOS_VARIAVEIS_MERCADORIA', 'Mercadoria para Revenda'),
    ('CUSTOS_VARIAVEIS_MATERIA_PRIMA', 'Matéria-prima'),
    ('CUSTOS_VARIAVEIS_INSUMOS', 'Insumos'),
    ('DESPESAS_OCUPACAO', 'Despesas com Ocupação'),
    ('DESPESAS_OCUPACAO_AGUA', 'Água'),
    ('DESPESAS_OCUPACAO_ALUGUEL', 'Aluguel'),
    ('DESPESAS_OCUPACAO_CONDOMINIO', 'Condomínio'),
    ('DESPESAS_OCUPACAO_TELEFONE_INTERNET', 'Telefone + Internet'),
    ('DESPESAS_OCUPACAO_IPTU', 'IPTU'),
    ('DESPESAS_OCUPACAO_LIMPEZA_CONSERVACAO', 'Limpeza e Conservação'),
    ('DESPESAS_OCUPACAO_ENERGIA_ELETRICA', 'Energia Elétrica'),
    ('DESPESAS_SERVICOS', 'Despesas com Serviços'),
    ('DESPESAS_SERVICOS_CONTABILIDADE', 'Contabilidade'),
    ('DESPESAS_SERVICOS_PUBLICIDADE_PROPAGANDA', 'Publicidade e Propaganda'),
    ('DESPESAS_SERVICOS_SERVICOS_JURIDICOS', 'Serviços Jurídicos'),
    ('DESPESAS_SERVICOS_WEBDESIGNER', 'Webdesigner'),
    ('DESPESAS_SERVICOS_DESIGNER', 'Designer'),
    ('DESPESAS_SERVICOS_SERVICOS_TI', 'Serviços de TI'),
    ('DESPESAS_PESSOAL', 'Despesas com Pessoal'),
    ('DESPESAS_PESSOAL_PRO_LABORE', 'Pró-Labore'),
    ('DESPESAS_PESSOAL_FOLHA_PAGAMENTO', 'Folha de Pagamento'),
    ('DESPESAS_PESSOAL_VALE_TRANSPORTE', 'Vale Transporte'),
    ('DESPESAS_PESSOAL_VALE_REFEICAO', 'Vale Refeição'),
    ('DESPESAS_PESSOAL_ASSISTENCIA_MEDICA', 'Assistência Médica'),
    ('DESPESAS_PESSOAL_ASSISTENCIA_ODONTO', 'Assistência Odonto'),
    ('DESPESAS_PESSOAL_INSS', 'INSS'),
    ('DESPESAS_PESSOAL_FGTS', 'FGTS'),
    ('DEDUCOES_VENDAS', 'Deduções sobre Vendas'),
    ('DEDUCOES_VENDAS_DAS_SIMPLES_NACIONAL', 'DAS - Simples Nacional'),
    ('DEDUCOES_VENDAS_PIS', 'PIS'),
    ('DEDUCOES_VENDAS_COFINS', 'COFINS'),
    ('DEDUCOES_VENDAS_ISS', 'ISS'),
    ('DEDUCOES_VENDAS_IPI', 'IPI'),
    ('DEDUCOES_VENDAS_ICMS', 'ICMS'),
    ('DEDUCOES_VENDAS_COMISSOES', 'Comissões'),
    ('IMPOSTOS_DIRETOS', 'Impostos Diretos'),
    ('IMPOSTOS_DIRETOS_IRPJ', 'IRPJ'),
    ('IMPOSTOS_DIRETOS_CSLL', 'CSLL'),
)

TIPO_PESSOA_CHOICES = (
        ('Pessoa Jurídica', 'Pessoa Jurídica'),
        ('Pessoa Física', 'Pessoa Física'),
    )

STATUS_CHOICES = (
        ('Em Aberto', 'Em Aberto'),
        ('Pago', 'Pago'),
    )

# Define choices for the year field
ANO_CHOICES = (
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
    # Add more years as needed
)

TIPO_CHOICES = (
        ('Receita', 'Receita'),
        ('Outros', 'Outros'),
    )

STATUS_PAGAMENTO_CHOICES = (
        ('Não Pago', 'Não Pago'),
        ('Pago', 'Pago'),
    )
SITUACOES = (
        ('AB', 'Aberto'),
        ('PG', 'Pago')
    )

CHOICES_BANCOS = (
        ('SANTANDER', 'SANTANDER'),
        ('BRADESCO', 'BRADESCO'),
        ('ITAU', 'ITAU'),
        ('CAIXA', 'CAIXA'),
        ('BANCO DO BRASIL', 'BANCO DO BRASIL'),
        ('PICPAY', 'PICPAY'),
        ('MERCADO PAGO', 'MERCADO PAGO'),
        ('SAFRA PAY', 'SAFRA PAY')
    )




class Cliente(models.Model):
    cd_cliente = models.AutoField(primary_key=True, verbose_name="Código")
    nm_cliente = models.CharField(max_length=255, verbose_name="Nome do Cliente")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")
    telefone = models.CharField(max_length=20, verbose_name="PIX_Telefone")
    email = models.EmailField(max_length=255, verbose_name="PIX_Email")
    tipo = models.CharField(max_length=15, choices=TIPO_PESSOA_CHOICES, verbose_name="Tipo")
    cnpj_cpf = models.CharField(max_length=18, verbose_name="PIX_CPF", unique=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    
    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nm_cliente
    

class Fornecedor(models.Model):
    cd_forncedor = models.AutoField(primary_key=True, verbose_name="Código")
    nm_fornecedor = models.CharField(max_length=255, verbose_name="Nome do Fornecedor")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(max_length=255, verbose_name="E-mail")
    tipo = models.CharField(max_length=15, choices=TIPO_PESSOA_CHOICES, verbose_name="Tipo")
    cnpj_cpf = models.CharField(max_length=18, verbose_name="CNPJ/CPF", unique=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    
    class Meta:
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nm_fornecedor    


def upload_to_produto(instance, filename):
    # Define o caminho onde a imagem do produto será armazenada
    return 'produtos/{0}/{1}'.format(instance.id_produto, filename)


class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True, verbose_name="ID Produto")
    nm_produto = models.CharField(max_length=255, verbose_name="Nome do Produto")
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )
    status_produto = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ativo', verbose_name="Status do Produto")
    dt_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor de Venda", null=True, blank=True)
    valor_producao = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Custo de Produção", null=True, blank=True)
    image = models.FileField(verbose_name="Foto do Produto", upload_to=upload_to_produto, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    
    def __str__(self):
        return self.nm_produto
    
    def calcular_lucro_percentual(self):
        if self.valor_venda and self.valor_producao:
            lucro = self.valor_venda - self.valor_producao
            lucro_percentual = (lucro / self.valor_producao) * 100
            return round(lucro_percentual, 2)
        return 0


    
    
class Receita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_index=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateTimeField(db_index=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, verbose_name="Nome do Pagador", db_index=True)
    forma_recebimento = models.CharField(max_length=90)
    situacao = models.CharField(max_length=2, choices=SITUACOES)
    observacoes = models.TextField()
    tipo_recebimento = models.CharField(
        verbose_name="Tipo de Recebimento",
        choices=TIPO_RECEITA,
        default='OUTRAS_RECEITAS',
        max_length=90,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em", db_index=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em", db_index=True)


    def __str__(self):
        return f"{self.usuario} | {self.get_tipo_recebimento_display()} | {self.data_entrada}"


# Updated upload_to function for Despesa (Expense)
def upload_to_despesa(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return f"Despesas/{now.strftime('%Y/%m/%Y%m%d%H%M%S')}{filename_ext.lower()}"

# Model for Despesa (Expense)
class Despesa(models.Model):
    id_despesa = models.AutoField(primary_key=True)
    nome_credor = models.ForeignKey(Fornecedor, on_delete = models.SET_NULL, blank = True, null = True, verbose_name="Nome do Fornecedor", db_index=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_index=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateTimeField(db_index=True)
    situacao = models.CharField(max_length=11, choices=STATUS_CHOICES, db_index=True)
    observacoes = models.TextField()
    tipo_despesa = models.CharField(verbose_name="Tipo de Despesa",choices=STATUS_PAGAMENTO,default='CONTAS',max_length=90)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Enviado em")
    modo_pag = models.CharField(verbose_name="Método de Pagamento",max_length=30,default="Cartão de Crédito",choices=TIPO_PAGAMENTO)
    image = models.FileField(verbose_name="Documento",upload_to=upload_to_despesa,validators=[validate_file_extension], blank=True, null=True)

    

    def __str__(self):
        return f"{self.usuario} | {self.data_vencimento} | {self.nome_credor}"
    
    
class Gasto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_gasto = models.DateTimeField()
    tipo_gasto = models.CharField(verbose_name="Tipo de Gasto",choices=TIPO_GASTO,default='CUSTOS_VARIAVEIS',max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.usuario} | {self.get_tipo_gasto_display()} | {self.data_gasto}"
    
class OrcamentoReceitas(models.Model):
    ano = models.IntegerField(choices=ANO_CHOICES, verbose_name="Ano")
    mes = models.CharField(max_length=3, verbose_name="Mês")
    receita_com_produtos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Receita com Produtos")
    receita_com_servicos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Receita com Serviços")
    outras_receitas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Outras Receitas")
    outras_receitas_2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Outras Receitas 2")
    outras_receitas_3 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Outras Receitas 3")
    receitas_financeiras = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Receitas Financeiras")
    receitas_totais = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Receitas Totais", editable=False)
    
    class Meta:
        unique_together = (("ano", "mes"),)
        verbose_name_plural = "Orçamento de Receitas"

    def save(self, *args, **kwargs):
        # Calculate the total revenue for the month
        self.receitas_totais = (
            self.receita_com_produtos +
            self.receita_com_servicos +
            self.outras_receitas +
            self.outras_receitas_2 +
            self.outras_receitas_3 +
            self.receitas_financeiras
        )
        super(OrcamentoReceitas, self).save(*args, **kwargs)

    def __str__(self):
        return f"Orçamento de Receitas - {self.ano} ({self.mes})"

class OrcamentoGastos(models.Model):
    ano = models.IntegerField(choices=ANO_CHOICES, verbose_name="Ano")
    mes = models.CharField(max_length=3, verbose_name="Mês")
    
    # Expense categories
    custos_variaveis = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Custos Variáveis")
    despesas_com_ocupacao = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Despesas com Ocupação")
    despesas_com_servicos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Despesas com Serviços")
    despesas_com_pessoal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Despesas com Pessoal")
    deducoes_sobre_vendas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Deduções sobre Vendas")
    impostos_diretos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Impostos Diretos")
    outras_despesas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Outras Despesas")
    outras_despesas_2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Outras Despesas 2")
    outras_despesas_3 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Outras Despesas 3")
    despesas_financeiras = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Despesas Financeiras")
    investimentos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Investimentos")
    gastos_totais = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Gastos Totais", editable=False)
    
    class Meta:
        unique_together = (("ano", "mes"),)
        verbose_name_plural = "Orçamento de Gastos"

    def save(self, *args, **kwargs):
        # Calculate the total expenses for the month
        self.gastos_totais = (
            self.custos_variaveis +
            self.despesas_com_ocupacao +
            self.despesas_com_servicos +
            self.despesas_com_pessoal +
            self.deducoes_sobre_vendas +
            self.impostos_diretos +
            self.outras_despesas +
            self.outras_despesas_2 +
            self.outras_despesas_3 +
            self.despesas_financeiras +
            self.investimentos
        )
        super(OrcamentoGastos, self).save(*args, **kwargs)

    def __str__(self):
        return f"Orçamento de Gastos - {self.ano} ({self.mes})"
        
# Model for Saldo Inicial
class SaldoInicial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    banco = models.CharField(max_length=100, verbose_name="Nome do Banco", choices=CHOICES_BANCOS)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo Inicial")
    data_inicial = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Enviado em")
       

    def __str__(self):
        return f"{self.usuario} | {self.banco} | {self.data_inicial}"

class SaldoAtual(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    banco = models.CharField(max_length=100, verbose_name="Nome do Banco", choices=CHOICES_BANCOS)
    saldo_atual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo Atual")
    data_atual = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")
    date_modificacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Transação")

    def __str__(self):
        return f"{self.usuario} | {self.banco} | {self.data_atual}"    
    

class LancamentoContasReceber(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, default=None)
    nr_documento = models.CharField(max_length=255, verbose_name="Numero Documento")
    data_dcto = models.DateField(verbose_name="Data Dcto")
    plano_conta = models.CharField(max_length=255, verbose_name="Plano de Conta")
    conta = models.CharField(max_length=255, verbose_name="Conta")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name="Tipo")
    descricao = models.TextField(verbose_name="Descrição")
    recebido_banco = models.BooleanField(default=False, verbose_name="Recebido pelo banco")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor R$")
    parcelas = models.IntegerField(verbose_name="Parcelas")
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Parcela")
    vencimento = models.DateField(verbose_name="Vencimento")
    recebimento = models.DateField(null=True, blank=True, verbose_name="Recebimento")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="Status")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    
    # Choices para o campo 'Status Recebimento'
    STATUS_RECEBIMENTO_CHOICES = (
        ('Não Recebido', 'Não Recebido'),
        ('Recebido', 'Recebido'),
    )
    status_recebimento = models.CharField(max_length=15, choices=STATUS_RECEBIMENTO_CHOICES, verbose_name="Status Recebimento")

    class Meta:
        verbose_name_plural = "Lançamentos Contas a Receber"

    def __str__(self):
        return self.documento
    

class LancamentoContasPagar(models.Model):
    despesa = models.ForeignKey(Despesa, on_delete = models.SET_NULL, blank = True, null = True, verbose_name="Despesa")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name="Fornecedor")
    documento = models.CharField(max_length=255, verbose_name="Numero Documento")
    data_docto = models.DateField(verbose_name="Data Dcto")
    plano_conta = models.CharField(max_length=255, verbose_name="Plano de Conta")
    conta = models.CharField(max_length=255, verbose_name="Conta")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name="Tipo")
    descricao = models.TextField(verbose_name="Descrição")
    pago_pelo_banco = models.BooleanField(default="SANTANDER",choices=CHOICES_BANCOS,  verbose_name="Pago pelo Banco")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor R$")
    parcelas = models.IntegerField(verbose_name="Parcelas")
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Parcela")
    vencimento = models.DateField(verbose_name="Vencimento")
    pagamento = models.DateField(null=True, blank=True, verbose_name="Pagamento")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="Status")
    status_pagamento = models.CharField(max_length=30, choices=STATUS_PAGAMENTO_CHOICES, verbose_name="Status do Pagamento",default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    

    class Meta:
        verbose_name_plural = "Lançamentos Contas a Pagar"

    def __str__(self):
        return self.documento       


