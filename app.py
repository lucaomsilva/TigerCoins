import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from src.data_handler import preparar_dados, baixar_dados
from src.model_train import treinar_modelo, prever_modelo, avaliar_modelo
from src.visualizer import grafico_predicao
import yfinance as yf
import time

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout. O layout "wide" usa mais espaço da tela.
st.set_page_config(
    page_title="TigerCoins - Sistema de Predição Financeira", page_icon="🐅", layout="wide"
)

# --- Barra Lateral (Sidebar) ---
# A barra lateral é usada para todos os inputs do usuário.

# --- Logo na Sidebar ---
try:
    logo = Image.open("./img/logo.png")
    st.sidebar.image(logo, use_container_width=True)
except FileNotFoundError:
    st.sidebar.error("Arquivo 'logo.png' não encontrado. Certifique-se de que ele está na mesma pasta do script.")

st.sidebar.markdown("---")

st.sidebar.title("Configurações de Predição")

st.sidebar.markdown("---")

# --- 1. Seleção de Ativos ---
st.sidebar.header("1. Seleção de Ativos")

# Lista de criptomoedas principais para o usuário escolher como alvo.
criptos_principais = [
    "BTC-USD",
    "ETH-USD",
    "ADA-USD",
    "SOL-USD",
    "XRP-USD",
    "DOGE-USD",
    "AVAX-USD",
]
cripto_alvo = st.sidebar.selectbox("Selecione a Criptomoeda Alvo:", criptos_principais)

# Lista de ativos que podem ser usados como variáveis adicionais.
ativos_externos = ["^GSPC", "DX-Y.NYB", "GC=F", "CL=F", "^IXIC", "^FTSE", "EURUSD=X"] + criptos_principais
ativos_auxiliares = st.sidebar.multiselect(
    "Selecione Ativos Auxiliares (Opcional):", ativos_externos
)

st.sidebar.markdown("---")

# --- 2. Configurações do Modelo ---
st.sidebar.header("2. Configurações do Modelo")

# Seleção do horizonte de predição em dias.
horizonte = st.sidebar.select_slider(
    "Horizonte de Predição (dias):", options=[1, 3, 5, 7], value=3
)

# Definição do tamanho da janela de dados para o modelo.
tamanho_janela = st.sidebar.number_input(
    "Tamanho da Janela de Análise (dias):", min_value=1, max_value=15, value=1, step=1
)

# Escolha entre prever o valor (regressão) ou a tendência (classificação).
tipo_saida = st.sidebar.radio(
    "Tipo de Saída Desejada:",
    ("Valor da Série (Regressão)", "Comportamento (Subida/Descida)"),
)

st.sidebar.markdown("---")

# --- 3. Seleção do Algoritmo ---
st.sidebar.header("3. Algoritmo de Predição")

# Lista de algoritmos de Machine Learning disponíveis.
algoritmos = ["Regressão Linear", "Random Forest", "KNN", "SVM", "XGBoost"]
algoritmo_selecionado = st.sidebar.selectbox("Selecione o Algoritmo:", algoritmos)

# Expander para configurações avançadas, que só aparece se o usuário clicar.
with st.sidebar.expander("Parametrização Avançada (Opcional)"):
    if algoritmo_selecionado == "Random Forest":
        n_estimators = st.slider("Número de Árvores:", 50, 500, 100, 10)
    elif algoritmo_selecionado == "KNN":
        n_neighbors = st.number_input("Número de Vizinhos (K):", min_value=1, max_value=10, value=1, step=1)
    elif algoritmo_selecionado == "SVM":
        svm_kernel = st.selectbox("Kernel do SVM:", ["linear", "rbf", "poly"])
    else:
        st.write("Sem parâmetros avançados para este modelo.")

st.sidebar.markdown("---")

# --- Exibir dados da cripto alvo na tela principal ---
# st.subheader(f"Visualização dos Dados de Fechamento - {cripto_alvo}")

data_inicio = "2022-01-01"
data_fim = "2024-04-01"

# try:
#     df_temp = baixar_dados(cripto_alvo, [], start=data_inicio, end=data_fim)
#     if df_temp.empty:
#         st.warning("⚠️ Nenhum dado disponível para o período selecionado.")
#     else:
#         # df_temp = df_temp.rename(columns={cripto_alvo: 'alvo'})
#         st.dataframe(df_temp.tail(15))  # Exibe os últimos 15 registros
# except Exception as e:
#     st.error(f"Erro ao carregar dados: {e}")

# --- Botão de Execução ---
# Este botão centraliza a ação do usuário para iniciar o processo.
executar = st.sidebar.button(
    "Executar Predição", type="primary", use_container_width=True
)

# --- Área Principal da Aplicação ---
st.title(f"Predição para {cripto_alvo}")
st.markdown(
    "Configure as opções na barra lateral à esquerda e clique em **Executar Predição** para iniciar."
)
# --- Exibir dados da cripto alvo na tela principal ---
st.subheader(f"Visualização dos Dados de Fechamento - {cripto_alvo}")

try:
    df_temp = baixar_dados(cripto_alvo, [])  # só a cripto alvo, sem auxiliares
    # df_temp = df_temp.rename(columns={cripto_alvo: 'alvo'})  # renomeia para consistência
    st.dataframe(df_temp.tail(15))  # mostra os últimos 15 registros
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")


# O código abaixo só será executado quando o botão for pressionado.
if executar:
    import numpy as np

    with st.spinner(f"Executando predição com {algoritmo_selecionado}... Por favor, aguarde."):
        # 1. Baixar dados
        df = baixar_dados(cripto_alvo, ativos_auxiliares, start=data_inicio, end=data_fim)
        df = df.rename(columns={cripto_alvo: 'alvo'})  # para padronizar target
        # 2. Preparar dados
        X, y = preparar_dados(
            df, 
            janela=tamanho_janela, 
            horizonte=horizonte, 
            target='alvo',
            tipo_saida='regressao' if tipo_saida.startswith("Valor") else 'classificacao'
        )
        # Usar 80% treino, 20% predição futura
        split = int(0.8 * len(X))
        if X.empty or y.empty:
            st.error("Erro: Dados insuficientes após o processamento. Tente reduzir o tamanho da janela ou o horizonte.")
            st.stop()

        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        # 3. Configurar parâmetros do modelo conforme escolhido
        params = {}
        if algoritmo_selecionado == "Random Forest":
            params['n_estimators'] = n_estimators
        elif algoritmo_selecionado == "KNN":
            params['n_neighbors'] = n_neighbors
        elif algoritmo_selecionado == "SVM":
            params['kernel'] = svm_kernel

        # 4. Treinar e prever
        modelo = treinar_modelo(X_train, y_train, algoritmo_selecionado, parametros=params)
        predicoes = prever_modelo(modelo, X_test)
        metrica = avaliar_modelo(y_test, predicoes)

        # 5. Construir DataFrames para plot
        datas = df.index[split + tamanho_janela + horizonte - 1:]

        print(df['alvo'].shape)
        print(type(df['alvo']))

        dados_historicos = pd.DataFrame({
            "Data": df.index[: split + tamanho_janela + horizonte - 1],
            "Preço": df['alvo'].iloc[: split + tamanho_janela + horizonte - 1, 0]
        })

        print(type(datas), np.shape(datas))
        print(type(predicoes), np.shape(predicoes))
        predicoes = predicoes.flatten()


        dados_predicao = pd.DataFrame({
            "Data": datas,
            "Preço": predicoes,
        })

        # --- Exibição dos Resultados ---
        st.subheader("Resultados da Predição")
        fig = grafico_predicao(dados_historicos, dados_predicao, nome_ativo=cripto_alvo)
        st.plotly_chart(fig, use_container_width=True)

        st.success("Predição concluída com sucesso!")

        # Métricas principais
        col1, col2 = st.columns(2)
        with col1:
            if algoritmo_selecionado == 'regressao':
                st.metric(label="Próximo Valor Previsto", value=f"${predicoes[0]:,.2f}")
            else:
                direcao = "Alta" if predicoes[0] == 1 else "Queda"
                st.metric(label="Próxima Tendência Prevista", value=direcao)
        with col2:
            if algoritmo_selecionado == 'regressao':
                st.metric(label="MAE", value=f"{metrica['MAE']:.2f}")
            else:
                try:
                    st.metric(label="Acurácia", value=f"{metrica['Accuracy']*100:.2f}%")
                except:
                    pass


else:
    st.info("Aguardando configuração e execução.")
