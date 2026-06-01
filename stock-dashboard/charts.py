import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data import TICKERS, COLORS, calcular_retorno_acumulado


def plot_preco_historico(dados: dict) -> go.Figure:
    fig = go.Figure()
    for ticker, nome in TICKERS.items():
        df = dados[ticker]
        close = df["Close"].dropna()
        fig.add_trace(go.Scatter(
            x=close.index,
            y=close.values,
            name=f"{nome} ({ticker.replace('.SA', '')})",
            line=dict(color=COLORS[ticker], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra></extra>",
        ))
    fig.update_layout(
        title="Cotação Histórica 2025 (R$)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
    )
    return fig


def plot_performance_comparativa(dados: dict) -> go.Figure:
    fig = go.Figure()
    for ticker, nome in TICKERS.items():
        retorno = calcular_retorno_acumulado(dados[ticker])
        fig.add_trace(go.Scatter(
            x=retorno.index,
            y=retorno.values,
            name=f"{nome} ({ticker.replace('.SA', '')})",
            line=dict(color=COLORS[ticker], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:.2f}%<extra></extra>",
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Performance Comparativa 2025 (% acumulado)",
        xaxis_title="Data",
        yaxis_title="Retorno (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
    )
    return fig


def plot_candlestick(dados: dict, ticker: str) -> go.Figure:
    df = dados[ticker].dropna()
    nome = TICKERS[ticker]

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.04,
    )

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Preço",
        increasing_line_color="#00B050",
        decreasing_line_color="#FF0000",
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        name="Volume",
        marker_color=COLORS[ticker],
        opacity=0.6,
    ), row=2, col=1)

    fig.update_layout(
        title=f"Candlestick — {nome} ({ticker.replace('.SA', '')})",
        xaxis_rangeslider_visible=False,
        yaxis_title="Preço (R$)",
        yaxis2_title="Volume",
        height=550,
        showlegend=False,
    )
    return fig
