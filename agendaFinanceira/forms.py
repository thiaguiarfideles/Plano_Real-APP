from django.forms import ModelForm
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import Cliente, Receita, Despesa, LancamentoContasPagar, Fornecedor, SaldoAtual, SaldoInicial, Produto
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from dal import autocomplete
from django_select2.forms import ModelSelect2Widget,Select2MultipleWidget
from django.forms.widgets import DateInput





class FornecedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FornecedorForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-fornecedor-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('index')
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(Field('nm_fornecedor'), css_class="col-md-6"),
                Div(Field('telefone'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('endereco'), css_class="col-md-6"),
                Div(Field('cidade'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('uf'), css_class="col-md-2"),
                Div(Field('tipo'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('email'), css_class="col-md-4"),
                css_class="row"),
            Div(
                Div(Field('cnpj_cpf'), css_class="col-md-3"),
                css_class="row"),
            Submit('submit', 'Enviar', css_class='btn-success col-centered')
        )
    class Meta:
        model = Fornecedor
        fields = ['nm_fornecedor','endereco','cidade','uf','telefone','email','tipo','cnpj_cpf']
        exclude=['cd_forncedor', 'usuario']
            
                

class ClienteForm(forms.ModelForm):
    
    class Meta:
        model = Cliente
        fields = ['nm_cliente', 'endereco', 'cidade', 'uf', 'telefone', 'email', 'tipo', 'cnpj_cpf']
        widgets = {
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Cidade'}),
            'uf': forms.TextInput(attrs={'placeholder': 'UF'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'cnpj_cpf': forms.TextInput(attrs={'placeholder': 'CNPJ/CPF'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nm_cliente'].required = True
        self.fields['telefone'].required = True
        self.fields['endereco'].required = False 
        self.fields['cidade'].required = False
        self.fields['uf'].required = False
        self.fields['email'].required = False
        self.fields['tipo'].required = False
        self.fields['cnpj_cpf'].required = False

class DespesaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DespesaForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-despesa-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('index')
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(Field('nome_credor'), css_class="col-md-6"),
                Div(Field('valor'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('data_vencimento'), css_class="col-md-6"),
                Div(Field('situacao'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('tipo_despesa'), css_class="col-md-2"),
                Div(Field('modo_pag'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('image'), css_class="col-md-4"),
                css_class="row"),
            Div(
                Div(Field('observacoes'), css_class="col-md-3"),
                css_class="row"),
            Submit('submit', 'Enviar', css_class='btn-success col-centered')
        )
    class Meta:
        model = Despesa
        fields = ['nome_credor','valor','data_vencimento','situacao','observacoes','tipo_despesa','modo_pag','image']
        exclude=['id_despesa', 'usuario','created_at']
        


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nm_produto', 'status_produto', 'valor_venda', 'valor_producao', 'image'] 
        widgets = {
            'dt_criacao': DateInput(attrs={'type': 'date'})
        }
        exclude = ['usuario']        
        


class ReceitaForm(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Produto.objects.all(), required=False)  

    class Meta:
        model = Receita
        fields = ['valor', 'cliente', 'data_entrada', 'forma_recebimento', 'situacao', 'observacoes', 'quantidade', 'produto']  
        widgets = {
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete'),
            'produto': autocomplete.ModelSelect2(url='produto-autocomplete'),
            'data_entrada': DateInput(attrs={'type': 'date'})
        }
        exclude = ['usuario', 'created_at']


class LancamentoContasPagarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LancamentoContasPagarForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-contasapagar-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('index')
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div(Field('data_docto'), css_class="col-md-3"),
                Div(Field('despesa'), css_class="col-md-4"),
                css_class="row"),
            Div(
                Div(Field('documento'), css_class="col-md-3"),
                Div(Field('plano_conta'), css_class="col-md-3"),
                Div(Field('conta'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('pago_pelo_banco'), css_class="col-md-4"),
                Div(Field('valor'), css_class="col-md-2"),
                Div(Field('parcelas'), css_class="col-md-2"),
                css_class="row"),
            Div(
                Div(Field('valor_parcela'), css_class="col-md-3"),
                Div(Field('vencimento'), css_class="col-md-3"),
                css_class="row"),
            Div(
                Div(Field('pagamento'), css_class="col-md-4"),
                Div(Field('status'), css_class="col-md-4"),
                css_class="row"),
            Div(
                Div(Field('tipo'), css_class="col-md-4"),
                Div(Field('fornecedor'), css_class="col-md-8"),
                css_class="row"),
            Div(
                Div(Field('descricao'), css_class="col-md-8"),
                css_class="row"),
            Submit('submit', 'Enviar', css_class='btn-success col-centered')
        )

    class Meta:
        model = LancamentoContasPagar
        fields = ['data_docto', 'documento', 'plano_conta', 'conta', 'documento', 'tipo', 'fornecedor',
                  'descricao', 'pago_pelo_banco', 'valor', 'parcelas', 'valor_parcela', 'vencimento', 'pagamento',
                  'status', 'despesa']
        widgets = {
            'fornecedor': Select2MultipleWidget,
        }
      

class SaldoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SaldoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-saldo-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div('banco', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div('saldo', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div('data_inicial', css_class="col-md-5"),
                css_class="row"),
            Submit('submit', 'Enviar', css_class='btn btn-success col-centered')
        )

    class Meta:
        model = SaldoInicial
        fields = ['banco','saldo','data_inicial']
        exclude = ['usuario','created_at']
        
class SaldoAtlForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SaldoAtlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-atual-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Div('banco', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div('saldo_atual', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div('data_atual', css_class="col-md-5"),
                css_class="row"),
            Submit('submit', 'Enviar', css_class='btn btn-success col-centered')
        )

    class Meta:
        model = SaldoAtual
        fields = ['banco','saldo_atual','data_atual']
        exclude = ['usuario', 'created_at']        
        
        