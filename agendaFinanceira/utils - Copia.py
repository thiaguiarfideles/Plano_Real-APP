import pandas as pd
from .models import Receita, Despesa

def get_financial_data():
    receitas_queryset = Receita.objects.all().values(
        'data_entrada', 'quantidade', 'valor', 'cliente__nm_cliente', 'forma_recebimento', 'situacao', 'observacoes'
    )
    df_receitas = pd.DataFrame(receitas_queryset)
    df_receitas.rename(columns={'data_entrada': 'data', 'quantidade': 'quantidade_receita', 'valor': 'valor_receita'}, inplace=True)

    despesas_queryset = Despesa.objects.all().values(
        'data_vencimento', 'valor', 'nome_credor__nm_fornecedor', 'situacao', 'observacoes', 'tipo_despesa', 'modo_pag'
    )
    df_despesas = pd.DataFrame(despesas_queryset)
    if not df_despesas.empty:
        df_despesas.rename(columns={'data_vencimento': 'data', 'valor': 'valor_despesa'}, inplace=True)
        df_despesas['quantidade_despesa'] = 1
    else:
        df_despesas['data'] = []
        df_despesas['valor_despesa'] = []
        df_despesas['quantidade_despesa'] = []

    return df_receitas, df_despesas

df_receitas, df_despesas = get_financial_data()

if not df_receitas.empty and not df_despesas.empty:
    df = pd.merge(df_receitas, df_despesas, on="data", how="outer").fillna(0)

    X = df[['quantidade_receita', 'valor_receita', 'quantidade_despesa', 'valor_despesa']]
    y = df['valor_receita'] - df['valor_despesa']

    print("Features (X):")
    print(X.head())
    print("Target (y):")
    print(y.head())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    with open('financial_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Modelo treinado e salvo como 'financial_model.pkl'")
else:
    print("Dados insuficientes para treino do modelo.")

