# data_handler.py

import pandas as pd
import yfinance as yf

def baixar_dados(cripto_alvo, ativos_auxiliares, start="2022-01-01", end="2024-04-01"):
    ativos_aux = list(ativos_auxiliares or [])
    if cripto_alvo in ativos_aux:
        ativos_aux.remove(cripto_alvo)
    ativos = [cripto_alvo] + ativos_aux

    dados = {}
    for ativo in ativos:
        try:
            df_ativo = yf.download(ativo, start=start, end=end, progress=False, auto_adjust=True)
            if df_ativo.empty or 'Close' not in df_ativo.columns:
                print(f"⚠️ Dados indisponíveis ou incompletos para {ativo}")
                continue
            dados[ativo] = df_ativo['Close']
        except Exception as e:
            print(f"❌ Erro ao baixar {ativo}: {e}")
            continue

    if not dados:
        print("❌ Nenhum dado foi carregado com sucesso.")
        return pd.DataFrame()

    df_final = pd.DataFrame(dados).dropna()
    return df_final

def preparar_dados(df, janela=3, horizonte=1, target='alvo', tipo_saida='regressao'):
    """
    Transforms time series DataFrame into features X and target y using windowing.
    For 'regressao', y is the future price; for 'classificacao', y is 1 or 0 indicating rise/fall.
    """
    X, y = [], []
    for i in range(len(df) - janela - horizonte + 1):
        # Flatten window of length `janela` for features
        X.append(df.iloc[i : i+janela].values.flatten())
        futuro = df[target].iloc[i + janela + horizonte - 1]   # target value at forecast horizon
        atual = df[target].iloc[i + janela - 1]                # target value at end of window
        if tipo_saida == 'regressao':
            y.append(futuro)
        else:
            y.append(int(futuro > atual))  # 1 = price went up, 0 = price went down
    X = pd.DataFrame(X)
    y = pd.Series(y)
    X = pd.DataFrame(X)

    # Remove colunas com NaN e força tudo a ser numérico
    X = X.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='any')

    # Se ainda estiver vazio, retorna X e y vazios
    if X.empty:
        return pd.DataFrame(), pd.Series(dtype='float64')

    y = pd.Series(y)
    return X, y