# visualizer.py

import plotly.graph_objects as go

def grafico_predicao(dados_historicos, dados_preditos, nome_ativo="Ativo"):
    fig = go.Figure()
    # Plot historical price curve
    fig.add_trace(go.Scatter(
        x=dados_historicos['Data'], y=dados_historicos['Preço'],
        mode='lines', name='Dados Históricos',
        line=dict(color='royalblue')
    ))
    # Plot prediction curve only if it's regression (continuous values)
    if not dados_preditos['Preço'].dropna().isin([0, 1]).all():
        fig.add_trace(go.Scatter(
            x=dados_preditos['Data'], y=dados_preditos['Preço'],
            mode='lines', name='Predição',
            line=dict(color='orange', dash='dash')
        ))
    fig.update_layout(
        title=f'Histórico e Predição para {nome_ativo}',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        legend_title='Legenda'
    )
    return fig
