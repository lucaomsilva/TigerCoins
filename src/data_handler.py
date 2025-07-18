# data_handler.py

import yfinance as yf
import pandas as pd

def baixar_dados(cripto_alvo, ativos_auxiliares, start="2022-01-01", end="2024-04-01"):
    # Filter out empty strings from the auxiliary assets list
    ativos_aux = [ativo for ativo in ativos_auxiliares if ativo]
    if cripto_alvo in ativos_aux:
        ativos_aux.remove(cripto_alvo)
    ativos = [cripto_alvo] + ativos_aux
    print("Ativos: ", ativos)

    if not ativos:
        print("❌ Nenhum ativo especificado para baixar.")
        return pd.DataFrame()

    try:
        dfs = []

        for ativo in ativos:
            print(f"\nBaixando dados de {ativo})...")
            try:
                df_temp = yf.download(ativo, start=start, end=end)
                if 'Close' not in df_temp.columns:
                    print(f"⚠️ Dados indisponíveis para {ativo}. Ignorando.")
                    continue
                df_temp = df_temp[['Close']].rename(columns={'Close': ativo})
                df_temp['date'] = df_temp.index.date
                dfs.append(df_temp.reset_index(drop=True))
            except Exception as e:
                print(f"❌ Erro ao baixar {ativo}: {e}")

        if not dfs:
            raise ValueError("❌ Nenhum dado foi carregado com sucesso.")

        df_final = dfs[0]
        for df in dfs[1:]:
            df_final = pd.merge(df_final, df, on='date', how='inner')

        return df_final

    except Exception as e:
        print(f"❌ Erro ao baixar dados: {e}")
        return pd.DataFrame()

    # df_final = df_final.dropna()
    # return df_final


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
    y = pd.DataFrame(y)

    # Remove colunas com NaN e força tudo a ser numérico
    X = X.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='any')
    y = y.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='any')

    # Se ainda estiver vazio, retorna X e y vazios
    if X.empty:
        return pd.DataFrame(), pd.Series(dtype='float64')

    # y = pd.Series(y)
    
    print(X)
    print(y)

    return X, y