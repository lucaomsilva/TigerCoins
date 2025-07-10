import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

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

# O código abaixo só será executado quando o botão for pressionado.
if executar:
    # --- LÓGICA DE EXECUÇÃO (PLACEHOLDER) ---
    # Aqui é onde você vai chamar as funções da Fase 1 e 3 do seu plano.
    # 1. Chamar data_handler.py para baixar os dados
    # 2. Chamar o pré-processamento e engenharia de características
    # 3. Chamar o model_trainer.py para treinar o modelo selecionado
    # 4. Chamar o visualizer.py para gerar os gráficos

    with st.spinner(
        f"Executando predição com {algoritmo_selecionado}... Por favor, aguarde."
    ):
        # Simulação de dados para o gráfico de exemplo
        # No seu projeto, estes dados virão do seu modelo.
        dados_historicos_exemplo = pd.DataFrame({
            "Data": pd.to_datetime([
                "2023-01-01",
                "2023-01-02",
                "2023-01-03",
                "2023-01-04",
                "2023-01-05",
            ]),
            "Preço": [20000, 20500, 20300, 21000, 20800],
        })
        dados_predicao_exemplo = pd.DataFrame({
            "Data": pd.to_datetime([
                "2023-01-05",
                "2023-01-06",
                "2023-01-07",
                "2023-01-08",
            ]),
            "Preço": [20800, 21200, 21500, 21300],
        })

        # --- Exibição dos Resultados ---
        st.subheader("Resultados da Predição")

        # Gráfico com Plotly
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dados_historicos_exemplo["Data"],
                y=dados_historicos_exemplo["Preço"],
                mode="lines",
                name="Dados Históricos",
                line=dict(color="royalblue"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=dados_predicao_exemplo["Data"],
                y=dados_predicao_exemplo["Preço"],
                mode="lines",
                name="Predição",
                line=dict(color="orange", dash="dash"),
            )
        )

        fig.update_layout(
            title=f"Histórico e Predição para {cripto_alvo}",
            xaxis_title="Data",
            yaxis_title="Preço (USD)",
            legend_title="Legenda",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("Predição concluída com sucesso!")

        # Placeholder para outras métricas e resultados
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Próximo Valor Previsto",
                value=f"${dados_predicao_exemplo['Preço'].iloc[1]:,.2f}",
            )
        with col2:
            st.metric(
                label="Tendência Prevista",
                value="Alta" if "Alta" in tipo_saida else "Subida",
            )

else:
    st.info("Aguardando configuração e execução.")
