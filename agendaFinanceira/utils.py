import pandas as pd
from .models import Receita, Despesa

def get_financial_data():
    receitas = Receita.objects.all().values()
    despesas = Despesa.objects.all().values()
    
    df_receitas = pd.DataFrame.from_records(receitas)
    df_despesas = pd.DataFrame.from_records(despesas)
    
    return df_receitas, df_despesas
